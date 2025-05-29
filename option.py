
class Option():

    def mod_text_given_action(self, text, actions):
        if actions:
            for action in actions:
                match action[0]:
                    case "need":
                        needs = ", ".join(action[1])
                        additional = f" (need {needs})"
                        text = text + additional
                    case "remove":
                        needs = ", ".join(action[1])
                        additional = f" (uses up {needs})"
                        text = text + additional
                    case "add":
                        pass
                    case _:
                        pass
        return text

    def __init__(self, text, target, actions):
        self.text = self.mod_text_given_action(text, actions)
        self.target = int(target)
        self.actions = actions
    
    def check_reqs(self, inventory):
        # Collate reqs from actions.
        reqs = []
        for action in self.actions:
            if action[0] == "need" or action[0] == "remove":
                for req in action[1]:
                    reqs.append(req)
        
        # Check all reqs fulfilled.
        failures = []
        for req in reqs:
            if req not in inventory.inv:
                failures.append(req)

        if failures:
            bool = False
            plaintext = ", ".join(failures)
            msg = f"You do not have the required: {plaintext}"
        else:
            bool = True
            msg = ""
        return (bool, msg)