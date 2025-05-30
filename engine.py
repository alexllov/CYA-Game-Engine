from parser import parse_lines, run_setup
from tokenizer import read_game_file
from option import Option

def run(data, namespace, start=1):
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
        options = []
        display_options = []
        for i, (text, target, actions) in enumerate(scene["options"]):
            option = Option(text, target, actions, namespace)
            display_options.append(f"{i+1}. {option.text}\n")
            options.append(option)
        
        print("".join(display_options))

        while True:
            try:
                choice = int(input("Choose: "))
                # If valid choice.
                if 1 <= choice <= len(scene["options"]):
                    # If meet reqs.
                    selected = options[choice-1]
                    results_check_req = selected.check_reqs(namespace)
                    if results_check_req[0]:
                        break
                    else:
                        print(results_check_req[1])
            except ValueError:
                pass
            print("Invalid choice. Try again.")
        
        # Update inv based on effects of selected option.
        selected.process_option(namespace)

        # Update scene based on option.
        _, next_scene, actions = scene["options"][choice-1]
        current_scene = int(next_scene)

def main():
    setup_filepath = "./Occult/setup.py"
    filename = "./Occult/Occult v6.cya"
    namespace = run_setup(setup_filepath)
    lines = read_game_file(filename)
    data = parse_lines(lines)
    run(data, namespace)

main()