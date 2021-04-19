import math

VERSION = "0dev"

sys_vars = dict([
    ("e", math.e),
    ("pi", math.pi),
    ("ans", 0),
    ])

free_vars = set(("", "b", "c", "d", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "W", "X", "Y", "Z"))
vars = dict([
        ("a", 0),
    ])

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
        print("\t*optional argument")
        return
    elif (command == "let"):
        with open("./docs/help/let") as helpfile:
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
    else: print(f"'{command}' help does not exist")

    return

def letCmd(command):
    var = command[0]

    if (var in vars):
        print(f"let error: variable {var} is already set to {vars.get(var)}")
        return
    else:
        return setCmd(command)

def setCmd(command):
    var = command[0]

    #if ("=" in command[1]):
    #    command[1] = command[1].replace("=", " ")
    #    command[1] = command[1].split()
    #    value = command[1][1]
    if (command[1].lower() == "be" or command[1].lower() == "="): command.pop(1)
    else:
        print("set/let error: missing 'be' / '=' keyword")
        return

    value = command[1]

    vars[var] = value
    return f"{var} = {value}"

def varsCmd(command):
    print(f"system variables: {sys_vars}\nuser variables: {vars}")
    return

def cmdParser(command):
    command = command.split() # splits command given into a list
    operator = command[0].lower() # sets operator var to the first keyword
    command.pop(0) # removes operator from commmand

    for i in command:
        if (
            "=" in i and
            len(i) > 1
        ):
            j = i.replace("=", " = ")
            j = j.split()
            k = command.index(i)
            command[k : k + 1] = j

    try:
        result = globals()[operator + "Cmd"](command)
    except KeyError:
        print(f"error: command '{operator}' does not exist")
        return
    return result

state = True

def CLI():
    print(f"### Welcome to chalk v{VERSION} ###\ntype 'help' for a list of commands") # welcome message

    while (state == True):
        command = input("\n~> ") # command input
        if (len(command) == 0): print ("CLI error: no command was given")

        if (command[-1] == ";"): # if command ends with ';' execute command without printing
            command = command.rstrip(";")
            cmdParser(command)
        else: # otherwise print command result
            result = cmdParser(command)
            if (result != None):
                print(result)

if __name__ == "__main__":
    CLI()