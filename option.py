# Holy Grail
# namespace[action["address"]].FUNCTION(action["method"], action["body"])

class Option():
    """
    Modules Extending Option REQUIRE the following:
        .mod_txt(method, items) -> ""
        .check_req(method, items) -> (true,_) OR (false,reason)
        .process(method, items) -> execute internal process
    """

    def create_req_list(self, namespace):
        """
        Processes the action list stored in option obj.
        Works out the property the action belongs to (from namespace),
        finds action method, & requred 'items' for said action.

        Returns array(dict): [{property, method, items}...]
        
        Req structure similar to HTTP request:
            property => address
            method => req method
            items => body
        """
        reqs = []
        print("sel.actions=", self.actions)

        for action in self.actions:
            # Split action into property its from & method
            # eg, i (player inv): add
            #     stat.str: ...

            # Search for module: filters base vs modules
            if "." in action[0]:
                property, action_method = action[0].split(".")
            else: 
                property = "base"
                action_method = action[0]
            property = namespace[property]

            # Split items from conditional decisions i present
            if "?" in action[1]:
                item_list, conditionals = action[1].split("?")
            else: conditionals = ""
            items = []
            # Collate items if present: mainly filtering base vs modules.
            for item in action[1]:
                items.append(item)

            reqs.append({"property": property,
                         "method": action_method,
                         "items": items,
                         "conditionals": conditionals})
        print(reqs)
        return reqs

    def mod_text_given_actions(self, text, namespace):
        """
        Takes original game text & game actions and modifies text according
        to rules given by the action's module.
        """
        #reqs = self.create_req_list(namespace)
        modifications = []
        for action in self.actions:
            mod = namespace[action["address"]].mod_txt(action["method"], action["body"])
            text += mod
        return text

    def __init__(self, text, target, actions, namespace):
        # Should be fine to do this as namespace shouldn't change after setup.
        # IF TRUE, then ++ self.reqs to streamline to 1 func call.
        self.namespace = namespace
        if target.isdigit():
            target = int(target)
        self.target = target
        # Actions = list of dicts
        self.actions = actions
        self.text = self.mod_text_given_actions(text, namespace)
    
    def __str__(self):
        return self.text

    def check_reqs(self, namespace):
        """
        Applies generic '.check_req' func across
        all reqs to ensure they're fulfilled.
        Returns (flag:bool & msg) (explaining failure if necessary)
        """

        # Check all reqs fulfilled.
        failures = []
        for action in self.actions:
            response = namespace[action["address"]].check_req(action["method"], action["body"])
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
        for action in self.actions:
            namespace[action["address"]].process(action["method"], action["body"])
