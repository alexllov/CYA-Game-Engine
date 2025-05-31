from parser import parse_lines, run_setup
from tokenizer import read_game_file
from option import Option


def generate_options(scene, namespace):
            options = []
            for i, (text, target, actions) in enumerate(scene["options"]):
                option = Option(text, target, actions, namespace)
                options.append(option)
            return options

def select_option(data, scene, namespace, options, old_scene=""):
    while True:

        for i, option in enumerate(options):
            print(f"{i+1}. {option}")
        print("Enter 'x' to open the menu.")
        
        try:
            choice = input("Choose: ")
            match choice:
                # If menu.
                case "x":
                    old_scene = scene
                    scene = data["MENU"]
                    # THIS ALL NEEDS TO => seperate handler func.
                    # currently not handling properly -> passing selected on
                    options = generate_options(scene, namespace)
                    selected, indx = select_option(data, scene, namespace, options, old_scene)
                    print("inside x case; select_option()")

                    pass
                case "s":
                    pass
                case "b":
                    pass
                # If valid index.
                case _ if choice.isdigit():
                    choice = int(choice)
                    selected = options[choice-1]
                    # If meet reqs.
                    results_check_req = selected.check_reqs(namespace)
                    if results_check_req[0]:
                        break
                    else:
                        print(results_check_req[1])
                case _:
                    pass
        except ValueError:
            pass
        print("Invalid choice. Try again.")
    indx = choice-1
    return selected, indx

def run(data, namespace):
    if "start" in namespace:
        start = namespace["start"]
    else:
        start = 1
    current_scene = start
    
    while True:
        scene = data[current_scene]
        if not scene:
            print(f"Error, scene {current_scene} not found, invalid location.")
            break
            
        print(f"\n {scene["text"]}")

        # Add a check if no options for end here.

        # Reformat to compile options then print as block
        # add "x for options menu" to end
        # remember to mod choice <= len to account for +1
        options = generate_options(scene, namespace)

        selected, indx = select_option(data, scene, namespace, options)
        
        # Update inv based on effects of selected option.
        selected.process_option(namespace)

        # Update scene based on option
        ###########################
        # update to scene[selected]
        _, next_scene, actions = scene["options"][indx]
        current_scene = int(next_scene)

def main():
    setup_filepath = "./Occult/setup.py"
    filename = "./Occult/Occult v6.cya"
    namespace = run_setup(setup_filepath)
    lines = read_game_file(filename)
    data = parse_lines(lines)
    # Graft data onto scenes s.t it has access to locs as well as namespace.
    namespace["base"].scenes = data
    run(data, namespace)

main()