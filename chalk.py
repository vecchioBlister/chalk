import math

VERSION = "0dev"

free_vars = set(("", "b", "c", "d", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "W", "X", "Y", "Z"))
variables = dict([
    ("ans", 0)
])

man_var = "ans" # currently manipulated variable
man_value = "" # currently manipulated variable value

def calculate(equation):

    return eval(equation)

def calcCmd(command):
    command = "".join(command) # concatenates command bac into a string
    if (command[0] == "="): command = command.lstrip("=") # strips "=" from command beginning
    #command = command.strip(" ") # strips whitespaces from command

    #allowed_chars = "0123456789+-*(). /"
    #for char in command:
    #    if char not in allowed_chars:
    #        errorMsg("calc", f"{char} is not a valid operator")
    #        return

    if (man_var in variables):
        variables[man_var] = calculate(command)
    else: # gives an error
        errorMsg("calc", f"'{man_var}' is not a valid variable")
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

    if (var in variables):
        errorMsg("let", f"variable {var} is already set to {variables.get(var)}")
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

    if (len(command) == 1): # if no value is given, man_value is taken
        value = man_value
    elif (command[1].lower() == "be" or command[1].lower() == "=" or command[1].lower() == "to"):
        command.pop(1)
        value = calculate(command[1])
    else:
        errorMsg("let/set", "missing 'be' / '=' / 'to' keyword")
        return

    variables[var] = value
    return f"{var} = {value}"

def varsCmd(command):
    print("assigned variables:")
    for i in variables:
        print(f"\t{i}\t=\t{variables.get(i)}")
    return

def varManUpd(): # updates the manipulated var string
    global man_var
    global man_value

    if (man_var in variables):
        man_value = variables.get(man_var)
    else:
        errorMsg("varManUpd", f"CRITICAL the variable {man_var} doesn't exist")
        return

    return

def manCmd(command):
    global man_var

    if (len(command) == 0):
        man_var = "ans"
        return "[ans] is now manipulated"
    var = command[0]

    if (var in variables):
        man_var = var
    else: # gives an error
        errorMsg("man", f"'{var}' is not a variable")
        return

    return f"[{var}] is now manipulated"

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
        command = input(f"\n[{man_var}]({man_value})> ") # command input
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