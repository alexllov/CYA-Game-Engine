from tokenizer import read_game_file

def parse_option(line):
    """
    Process option line, produces 3 parts: text, target, actions:
        text: the plaintext of the option presented.
        target: destination upon selecting option.
        actions: game events triggered by selecting option.
    """
    # Pull off text
    text, rest = line.split("->")
    text = text[1:].strip()

    # Separate Target from reqs
    rest = rest.strip()
    parts = rest.split(" ",1)
    target = parts[0]
    flags = parts[1] if len(parts) > 1 else False
    actions = []

    if flags:
        # Clean & partition flags.
        flags = flags.split("][")
        flags = list(
            map(
                lambda x: x.strip("[").strip("]"),
                flags
            )
        )

        # Process each flag
        for flag in flags:
            parts = flag.split(" ", 1)
            action = parts[0]
            items = parts[1] if len(parts) > 1 else ""
            # Split list of items, strip to clean, -> clean list of items.
            items = list(
                map(
                    lambda x: x.strip(),
                    list(items.split(","))
                )
            )
            actions.append((action, items))
    return (text, target, actions)


def parse_lines(lines):
    """
    Processes lines, builds JSON style obj of scenes with text and options.
    """
    modules = {}
    data = {}
    current_scene = None
    text_lines = []
    options = []

    for line in lines:
        line = line.strip()

        # Skip whitespace & comments.
        if line == "" or line.startswith("#"):
            continue

        # Pull out imports to dict.
        elif line.startswith("import"):
            line = line.replace("import", "", 1).strip()
            if " as " in line:
                module, pseudo = line.split(" as ")
                modules[pseudo] = module
            else:
                module = line
                modules[module] = module

        # ID the start of scenes.
        elif line.isdigit():
            if current_scene is not None:
                data[current_scene] = {
                    "text": "\n".join(text_lines),
                    "options": options
                }
            current_scene = int(line)
            text_lines = []
            options = []

        # ID options.
        elif line.startswith(">"):
            option = parse_option(line)
            options.append(option)
        
        # Grab texts.
        elif line.startswith('"') or line.startswith("'"):
            text_lines.append(line)

        # Here is where lang instructions will be gathered.
        # Hotwiring this here to collect non INT IDs
        else:
            if current_scene is not None:
                data[current_scene] = {
                    "text": "\n".join(text_lines),
                    "options": options
                }
            current_scene = line
            text_lines = []
            options = []


    if current_scene is not None:
        data[current_scene] = {
            "text": "\n".join(text_lines),
            "options": options
        }
    
    data["modules"] = modules

    return data


def run_setup(filepath):
    """
    Constructs namespace store to track values & modules used within game code.
    """
    with open(filepath, "r") as file:
        code = file.read()
    namespace = {}
    exec(code, namespace)
    del namespace["__builtins__"]
    """
    # base is protected name for core funcs.
    #namespace["base"] = Base()
    """
    return namespace


if __name__ == "__main__":
    namespace = run_setup("./Occult/setup.py")
    print(namespace)
    lines = read_game_file("./Occult/Occult v6.cya")
    scenes = parse_lines(lines)
    print(scenes)