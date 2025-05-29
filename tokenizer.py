
def read_game_file(filename: str):
    """
    Takes filepath, returns list of split lines.
    """
    with open(filename, "r") as file:
        lines = file.read().split("\n")
    return lines


if __name__ == "__main__":
    print(read_game_file("./Occult v4.cya"))