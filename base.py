
class Base():
    def __init__(self, namespaec):
        self.contents = []


    # BASE MAY NEED SPECIAL TREATMENT & ACCESS TO THE NAMESPACE TO HANDLE xyz
    # OR JUST MAKE OBJ NOW?
    def contents(self):
        print(self.contents)

    def mod_txt(method, items):
        return ""

    def check_req(method, items):
        return (True, "")

    def process(method, items):
        match method:
            case "save":
                print("SAVE WIP")
                ...
            case "contents":
                contents()


