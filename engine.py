from parser import parse_lines
from tokenizer import read_game_file
from option import Option
from inventory import Inventory


def run(scenes, start=1):
    current_scene = start
    inventory = Inventory()

    while True:
        scene = scenes[current_scene]
        if not scene:
            print(f"Error, scene {current_scene} not found, invalid location.")
            break
            
        print(f"\n {scene["text"]}")

        # Add a check if no options for end here.

        # Reformat to compile options then print as block
        # add "x for options menu" to end
        # remember to mod choice <= len to account for +1
        options = []
        for i, (text, target, actions) in enumerate(scene["options"]):
            option = Option(text, target, actions)
            print(f"{i+1}. {option.text}")
            options.append(option)

        while True:
            try:
                choice = int(input("Choose: "))
                # If valid choice.
                if 1 <= choice <= len(scene["options"]):
                    # If meet reqs.
                    selected = options[choice-1]
                    results_check_req = selected.check_reqs(inventory)
                    if results_check_req[0]:
                        break
                    else:
                        print(results_check_req[1])
            except ValueError:
                pass
            print("Invalid choice. Try again.")
        
        # Update inv based on effects of selected option.
        inventory.process_option(selected)

        # Update scene based on option.
        _, next_scene, actions = scene["options"][choice-1]
        current_scene = int(next_scene)


def main():
    filename = "./Occult v4.cya"
    lines = read_game_file(filename)
    scenes = parse_lines(lines)
    run(scenes)

main()