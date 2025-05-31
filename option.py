# Holy Grail
# req["property"].FUNCTION(req["method"], req["items"])

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

            items = []
            # Collate items if present: mainly filtering base vs modules.
            for item in action[1]:
                items.append(item)

            reqs.append({"property": property,
                         "method": action_method,
                         "items": items})
        return reqs

    def mod_text_given_actions(self, text, actions, namespace):
        """
        Takes original game text & game actions and modifies text according
        to rules given by the action's module.
        """
        reqs = self.create_req_list(namespace)
        modifications = []
        for req in reqs:
            mod = req["property"].mod_txt(req["method"], req["items"])
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
            response = req["property"].check_req(req["method"], req["items"])
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
            req["property"].process(req["method"], req["items"])
