import math

VERSION = "0dev"

free_vars = set(("a", "b", "c", "d", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "W", "X", "Y", "Z"))
variables = dict([
    ("ans", 0)
])

man_var = "ans" # currently manipulated variable
man_value = "" # currently manipulated variable value

def calculate(command):
    operators = "+-*().,; /[]"

    #if (type(command) == list):
    #    for i in range(len(command)): # turns every element in command list and makes it a string
    #        command[i] = str(command[i])
    #else: command = list(str(command)) # if input is not list, makes it a list of string

    if (type(command) is int):
        command = str(command)
    command = list(command)

    if (len(command) == 0): return 0 # if input is empty, returns 0

    for i in range(len(command)):
        if (command[i] == "math.pi"): # replaces math.py variables
            command[i] = str(math.pi)
        elif (command[i] == "math.e"):
            command[i] = str(math.e)
        elif (command[i] in variables): # replaces long-name variables with their values
            try:
                command[i] = calculate(variables.get(command[i]))
            except RecursionError as error: # when a lazy var is assigned to itself
                errorMsg("calc", "cannot calculate a variable with self assignment")
                print(error)
                return None
            if (type(command[i]) == list):
                if (len(command) == 1): command[i] = command[i][0] # if item is a list with one element, takes first
                else:
                    errorMsg("calc", "cannot multiply for an array")
            elif (command[i] is None): return None # in case of calculate() error
            command[i] = str(command[i])

    command = "".join(str(j) for j in command) # concatenates command back into a string
    #//print(command)
    equation = ""
    for i in command:
        #if (i in variables): # replaces variables with their values
        #    equation.append(str(calculate(variables.get(i))))
        if (i.isalpha() and not i in operators):
            errorMsg("calc", f"{i} symbol / variable name ambiguity")
            return None
        else:
            #//print(i)
            equation += i

    #//print(equation)
    #equation = "".join(str(j) for j in equation) # concatenates equation back into a string
    #equation = equation.format_map(variables) # replaces variables with their values
    equation = equation.strip() # strips whitespaces from equation

    try:
        #//print(equation)
        return eval(equation)
    except SyntaxError as error:
        errorMsg("calc", f"cannot understand operation. \n{error}")
        return None
    except TypeError as error:
        errorMsg("calc", f"{error}")
        return None

def calcCmd(command):
    if (man_var in variables):
        result = calculate(command)
        if (result is None): return
        else: variables[man_var] = result
    else: # gives an error
        errorMsg("calc", f"'{man_var}' is not a valid variable (man)")
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
    elif (command == "var"):
        with open("./docs/help/var") as helpfile:
            printHelp(helpfile)
        return
    else: errorMsg("help", f"'{command}' help does not exist")

    return

def letCmd(command):
    if (len(command) == 0): # if no variable is given, calls setCmd() to assign a new one
        return setCmd(command)

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
    if (len(command) == 0): # if no variable is given, a free one is assigned
        command.append(free_vars.pop())

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
    for i in var:
        if (not i.isalpha()):
            errorMsg("let/set", "variable names cannot contain digits or symbols")
            return

    if (var.isdigit()):
        errorMsg("let/set", "cannot assign value to a number")
        return

    if (var in free_vars): # removes var from free_vars when it is assigned
        free_vars.remove(var)

    if (len(command) == 1): # if no value is given, man_value is taken
        value = man_value
    elif (command[1].lower() != "be" and command[1].lower() != "=" and command[1].lower() != "to"):
        errorMsg("let/set", "missing 'be' / '=' / 'to' keyword")
        return
    else:
        command.pop(1)
        if (command[1][0] == "&"):
            value = ""
            command[1] = command[1].lstrip("&")
            for i in range(1, len(command)):
                if (command[i] != ""):
                    value += str(command[i]) + " "
                #value = " ".join(command[i])
            value = value.rstrip()
            variables[var] = value
            return f"(lazy) {var} = {value}"
        #if (command[1] != "("): #?????
        #    value = calculate(command[1 : None])
        #    if (value is None):
        #        return
    value = calculate(command[1 : None])
    if (value is None):
        errorMsg("let/set", "cannot assign empty variable")
        return

    variables[var] = value
    return f"{var} = {value}"

def varCmd(command):
    if (len(command) == 0):
        print("assigned variables:")
        for i in variables:
            print(f"\t{i}\t=\t{variables.get(i)}")
        return
    else:
        for i in range(len(command)):
            command[i].split(",")
        for i in command:
            if (i in variables):
                print(f"\t{i}\t=\t{variables.get(i)}")
            else:
                print(f"{i} is not an assigned variable")

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
        command[0] = command[0].lstrip("=") # strips "=" from command beginning
        return calcCmd(command)

    command.pop(0) # removes operator from commmand

    try:
        return globals()[operator + "Cmd"](command)
    except KeyError as error:
        errorMsg("cmdParser", f"command '{operator}' does not exist")
        print(error)
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