from random import randint as r

def mod_txt(method, items):
    return ""

def check_req(method, items):
    return (True, "")

def roll(num, size, mod):
    """
    Roll num dice of size size & + mod to result.
    """
    a = mod
    for i in range(num):
        a += r(1,size)
    return a

def roll_dice(method):
    mod = 0
    # Process modifier if present.
    if "+" in method:
        roll_req, mod = method.split("+")
        method = roll_req
    if "-" in method:
        roll_req, mod = method.split("-")
        mod = -mod
        method = roll_req

    # Split on the d: 1d6 -> num, size
    if "d" in method:
        a, b = method.split("d")
    else: ValueError

    if a.isdigit() and b.isdigit():
        # Number of Dice
        number = int(a)
        # Size of Dice
        size = int(b)
    result = roll(number, size, mod)
    return result

def process(method, items):
    """
    THIS WILL NEED TO BE EXPANDED / GENERALISED IN FUTURE S.T. WE CAN GET INTS
    FROM ITEMS THAT -> STATE VARS RATHER THAN BEING INTS.
    
    Limit to 1 item in items

    Takes:
        method in the format 1d6+mod
        condition for roll, if for a check, in the format <x or >x
    """
    result = roll_dice(method)
    item = items[0]

    #################
    # Add code here 4 turn obj val -> "[CONT]int"
    #################

    match item:
        case _ if ">" in item:
            item = item.strip(">")
            item = int(item)
            succ = False
            if result > item:
                succ = True
                print(f"You passed!")
            else: print("you failed")
            return succ

        case _ if "<" in item:
            item = item.strip("<")
            item = int(item)
            succ = False
            if result < item:
                succ = True
                print("You passed!")
            else: print("You failed")
            return succ
        
        case _:
            print(f"{result=}")
            return result