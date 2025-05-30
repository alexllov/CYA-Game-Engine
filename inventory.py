
class Inventory():
    """
    Provides storage for the Player through a dict.
    Options module.
    """

    def __init__(self):
        self.inv = {}
    
    def __str__(self):
        return f"{self.inv}"

    def process(self, type, items):
        """
        Processes the action req upon taking linked option.
        """
        match type:
            case "need":
                pass
            case "add":
                for item in items:
                    self.add(item)
            case "remove":
                for item in items:
                    self.remove(item)
            case "menu":
                self.menu()
            case _:
                pass
    
    def mod_txt(self, type, items):
        """
        Modifies base option text based on action impact.
        """
        match type:
            case "need":
                needs = ", ".join(items)
                additional = f" (need {needs})"
                return additional
            case "add":
                return ""
            
            case "remove":
                needs = ", ".join(items)
                additional = f" (uses up {needs})"
                return additional
            case _:
                ValueError
    
    def add(self, item):
        """
        Adds item to inventory.
        """
        if item in self.inv:
            self.inv[item] += 1
        else:
            self.inv[item] = 1

    def remove(self, item):
        """
        Removes item from inventory.
        """
        if item in self.inv:
            self.inv[item] -= 1
        else:
            ValueError
        if self.inv[item] <= 0:
            del self.inv[item]
    
    def check_items(self, reqs):
        """
        Check if inventory contains the required items.
        Returns (True, _) OR (False, message explaining missing items)
        """
        failures = []
        for item in reqs:
            if item not in self.inv:
                failures.append(item)
        if failures:
            flag = False
            plaintext = ", ".join(failures)
            msg = f"You do not have the required: {plaintext}"
        else:
            flag = True
            msg = ""
        return (flag, msg)

    def check_req(self, type, reqs):
        """
        Checks if inventory matches stated requirement
        (contains the required items).
        """
        match type:
            case "add":
                return (True, "")
            case "need":
                response = self.check_items(reqs)
                return response
            case "remove":
                response = self.check_items(reqs)
                return response
            case _:
                ValueError
    
    def menu(self):
        """
        TODO
        Display Inventory for Menu. Edit this in future.
        """
        print(self)