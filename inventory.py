
class Inventory():

    def __init__(self):
        self.inv = {}
    
    def __str__(self):
        return f"{self.inv}"

    def process(self, type, items):
        match type:
            case "need":
                pass
            case "add":
                for item in items:
                    self.add(item)
            case "remove":
                for item in items:
                    self.remove(item)
            case _:
                pass
    
    def mod_txt(self, type, items):
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
    
    def check_items(self, reqs):
        failures = []
        for item in reqs:
            if item not in self.inv:
                failures.append(item)
        if failures:
            bool = False
            plaintext = ", ".join(failures)
            msg = f"You do not have the required: {plaintext}"
        else:
            bool = True
            msg = ""
        return (bool, msg)

    def check_req(self, type, reqs):
        match type:
            case "add":
                return True
            case "need":
                response = self.check_items(reqs)
                return True
            case "remove":
                response = self.check_items(reqs)
                return True
            case _:
                ValueError