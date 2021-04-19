import math

VERSION = "0dev"

sys_vars = dict([
    ("ans", 0),
    ("e", math.e),
    ("pi", math.pi),
    ])

free_vars = set(("", "b", "c", "d", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "W", "X", "Y", "Z"))
user_vars = dict([])

manip_var = "ans" # currently manipulated variable
manip_value = "" # currently manipulated variable value

def calcCmd(command):
    command = "".join(command) # concatenates command bac into a string
    if (command[0] == "="): command = command.lstrip("=") # strips "=" from command beginning
    #command = command.strip(" ") # strips whitespaces from command

    allowed_chars = "0123456789+-*(). /"
    for char in command:
        if char not in allowed_chars:
            errorMsg("calc", f"{char} is not a valid operator")

    if (manip_var in user_vars): # checks if it is a user var
        user_vars[manip_var] = eval(command)
    elif (manip_var in sys_vars): # checks if it is a system var
        sys_vars[manip_var] = eval(command)
    else: # gives an error
        errorMsg("calc", f"'{manip_var}' is not a valid variable")
        return


    return

def exitCmd(command):
    # closes chalk by setting state to False
    global state
    state = False
    return "bye"

def printHelp(helpfile):
    # prints each line of helpfile, formatting the variables
    for i in helpfile:
        print(i.rstrip().format(
            VERSION = VERSION,
            ))
    return

def helpCmd(command):
    # calls printHelp() with the chosen helpfile

    if (len(command) == 0): # prints the main help page (no argument given)
        with open("./docs/help/help") as helpfile:
            printHelp(helpfile)
        return
    else: command = command[0] # otherwise chooses the first argument

    if (command == "me"): # :)
        print("oh no")
        return
    elif (command == "exit"):
        print("exit")
        print("\tcloses chalk.")
        return
    elif (command == "help"):
        print("help *<command>")
        print("\tprints the main help page or a specific <command> help page.")
        return
    elif (command == "let"):
        with open("./docs/help/let") as helpfile:
            printHelp(helpfile)
        return
    elif (command == "man"):
        with open("./docs/help/man") as helpfile:
            printHelp(helpfile)
        return
    elif (command == "set"):
        with open("./docs/help/set") as helpfile:
            printHelp(helpfile)
        return
    elif (command == "vars"):
        with open("./docs/help/vars") as helpfile:
            printHelp(helpfile)
        return
    else: errorMsg("help", f"'{command}' help does not exist")

    return

def letCmd(command):
    if (len(command) == 0):
        errorMsg("let/set", "no variable was given")
        return

    for i in command:
        if (
            "=" in i and
            len(i) > 1
        ):
            j = i.replace("=", " = ")
            j = j.split()
            k = command.index(i)
            command[k : k + 1] = j

    var = command[0]

    if (var in user_vars):
        errorMsg("let", f"variable {var} is already set to {user_vars.get(var)}")
        return
    else:
        return setCmd(command)

def setCmd(command):
    if (len(command) == 0):
        errorMsg("let/set", "no variable was given")
        return

    for i in command:
        if (
            "=" in i and
            len(i) > 1
        ):
            j = i.replace("=", " = ")
            j = j.split()
            k = command.index(i)
            command[k : k + 1] = j

    var = command[0]

    if (var.isdigit()):
        errorMsg("let/set", "cannot assign value to a number")
        return
    if (var in sys_vars):
        errorMsg("let/set", f"variable {var} is a system variable set to {sys_vars.get(var)}")
        return


    if (command[1].lower() == "be" or command[1].lower() == "=" or command[1].lower() == "to"): command.pop(1)
    else:
        errorMsg("let/set", "missing 'be' / '=' / 'to' keyword")
        return

    value = command[1]
    if (not value.isdigit()): # checks if "value" contains chars other than numbers
        if (value in user_vars): # checks if it is a user var
            value = user_vars.get(value)
        elif (value in sys_vars): # checks if it is a system var
            value = sys_vars.get(value)
        else: # gives an error
            errorMsg("let/set", f"'{value}' is not a number or a variable")
            return

    user_vars[var] = value
    return f"{var} = {value}"

def varsCmd(command):
    print("system variables:")
    for i in sys_vars:
        print(f"\t{i}\t=\t{sys_vars.get(i)}")
    print("\nuser variables:")
    for j in user_vars:
        print(f"\t{j}\t=\t{user_vars.get(j)}")
    return

def varManUpd(): # updates the manipulated var string
    global manip_var
    global manip_value

    if (not manip_var.isdigit()): # checks if "var" contains chars other than numbers
        if (manip_var in sys_vars):
            manip_value = sys_vars.get(manip_var)
        elif (manip_var in user_vars):
            manip_value = user_vars.get(manip_var)
    else: manip_value = manip_var

    return

def manCmd(command):
    global manip_var

    if (len(command) == 0):
        manip_var = "ans"
        return "[ans] is manipulated"
    var = command[0]

    if (not var.isdigit()): # checks if "var" contains chars other than numbers
        if (var in user_vars): # checks if it is a user var
            manip_var = var
        elif (var in sys_vars): # checks if it is a system var
            manip_var = var
        else: # gives an error
            errorMsg("man", f"'{var}' is not a number or a variable")
            return
    else: manip_var = var

    return f"[{var}] is manipulated"

def cmdParser(command):
    command = command.split() # splits command given into a list
    operator = command[0] # sets operator var to the first keyword

    if (operator[0] == "="):
        return calcCmd(command)

    command.pop(0) # removes operator from commmand

    try:
        return globals()[operator + "Cmd"](command)
    except KeyError:
        errorMsg("cmdParser", f"command '{operator}' does not exist")
        return

def errorMsg(module, message):
    print(f"<!> {module} error: {message}")
    return

state = True

def CLI():
    print(f"### Welcome to chalk v{VERSION} ###\ntype 'help' for a list of commands") # welcome message

    while (state is True):
        varManUpd()
        command = input(f"\n[{manip_value}]" + "> ") # command input
        if (len(command) == 0 or command.split() == []): errorMsg("CLI", "no command was given")
        else:
            if (command[-1] == ";"): # if command ends with ';' execute command without printing
                command = command.rstrip(";")
                cmdParser(command)
            else: # otherwise print command result
                result = cmdParser(command)
                if (result != None):
                    print(result)

if __name__ == "__main__":
    CLI()