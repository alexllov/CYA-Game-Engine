class Menu():
    def __init__(self, return_loc, data):
        self.return_loc = return_loc
        self.contents = {}
        for key in data:
            if type(key) != int:
                self.contents[key] = data[key]

        self.options = ["Enter 'c' to go to Contents page.",
                        "Enter 's' to Save Game.",
                        "Enter 'b' to go back to the game."]

    def execute(self):
        while True:
            print(self.options)
            i = input("")