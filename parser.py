from tokenizer import read_game_file


def parse_option(line):
    """
    Process option line.
    """
    # Pull off text
    text, rest = line.split("->")
    text = text[1:].strip()

    # Separate Target from reqs
    rest = rest.strip()
    try:
        target, flags = rest.split(" ",1)
    except:
        target = rest.strip()
        flags = False
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
            action, items = flag.split(" ", 1)
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
    scenes = {}
    current_scene = None
    text_lines = []
    options = []

    for line in lines:
        line = line.strip()

        if line == "" or line.startswith("#"):
            continue

        elif line.isdigit():
            if current_scene is not None:
                scenes[current_scene] = {
                    "text": "\n".join(text_lines),
                    "options": options
                }
            current_scene = int(line)
            text_lines = []
            options = []

        elif line.startswith(">"):
            option = parse_option(line)
            options.append(option)
        
        else:
            text_lines.append(line)

    if current_scene is not None:
        scenes[current_scene] = {
            "text": "\n".join(text_lines),
            "options": options
        }
    return scenes


if __name__ == "__main__":
    lines = read_game_file("./Occult v4.cya")
    scenes = parse_lines(lines)
    print(scenes)