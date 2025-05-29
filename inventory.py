
class Inventory():

    def __init__(self):
        self.inv = {}

    def process_option(self, option):
        print("inv, process_option", option.actions)
        for action in option.actions:
            match action[0]:
                case "need":
                    pass
                case "add":
                    for item in action[1]:
                        self.add(item)
                case "remove":
                    for item in action[1]:
                        self.remove(item)
                case _:
                    pass
    
    def add(self, item):
        if item in self.inv:
            self.inv[item] += 1
        else:
            self.inv[item] = 1

    def remove(self, item):
        if item in self.inv:
            self.inv[item] -= 1
        else:
            ValueError
        if self.inv[item] <= 0:
            del self.inv[item]