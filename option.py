# Holy Grail
# req["property"].FUNCTION(req["type"], req["items"])

import base

class Option():
    """
    Modules Extending Option REQUIRE the following:
        .mod_txt(type, items) -> ""
        .check_req(type, items) -> true,_ OR false,reason
        .process(type, items) -> execute internal process
    """

    def create_req_list(self, namespace):
        """
        Processes the action list stored in option obj.
        Works out the property the action belongs to (from namespace),
        finds action type, & requred 'items' for said action.

        Returns array(dict): [{property, type, items}...]
        """
        reqs = []
        for action in self.actions:
            # Split action into property its from & type
            # eg, i (player inv): add
            #     stat.str: ...

            # Search for module: filters base vs modules
            if "." in action[0]:
                property, action_type = action[0].split(".")
            else: 
                property = "base"
                action_type = action[0]
            property = namespace[property]

            items = []
            # Collate items if present: mainly filtering base vs modules.
            if len(action) > 1:
                for item in action[1]:
                    items.append(item)
            reqs.append({"property": property,
                         "type": action_type,
                         "items": items})
        print(reqs)
        return reqs

    def mod_text_given_actions(self, text, actions, namespace):
        """
        Takes original game text & game actions and modifies text according
        to rules given by the action's module.
        """
        reqs = self.create_req_list(namespace)
        modifications = []
        for req in reqs:
            mod = req["property"].mod_txt(req["type"], req["items"])
            text += mod
        return text

    def __init__(self, text, target, actions, namespace):
        # Should be fine to do this as namespace shouldn't change after setup.
        # IF TRUE, then ++ self.reqs to streamline to 1 func call.
        self.namespace = namespace
        if target.isdigit():
            target = int(target)
        self.target = target
        self.actions = actions
        self.text = self.mod_text_given_actions(text, actions, namespace)
    
    def __str__(self):
        return self.text

    def check_reqs(self, namespace):
        """
        Applies generic '.check_req' func across
        all reqs to ensure they're fulfilled.
        Returns (flag:bool & msg) (explaining failure if necessary)
        """
        reqs = self.create_req_list(namespace)  
        # Check all reqs fulfilled.
        failures = []
        for req in reqs:
            response = req["property"].check_req(req["type"], req["items"])
            if not response[0]:
                failures.append(response[1])

        # Needs rewrite to show appropriate err msgs.
        if failures:
            flag = False
            msg = ", ".join(failures)
        else:
            flag = True
            msg = ""
        return (flag, msg)
    
    def process_option(self, namespace):
        """
        The option is completed,
        necessary requirements are now "taken"/performed.
        """
        reqs = self.create_req_list(namespace)
        for req in reqs:
            req["property"].process(req["type"], req["items"])
