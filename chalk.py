import os
import time
import math

VERSION = "0dev"

free_vars = set(("a", "b", "c", "d", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "W", "X", "Y", "Z"))
variables = dict([
    ("ans", 0)
])

man_var = "ans" # currently manipulated variable
man_value = "" # currently manipulated variable value

state = True # CLI "on" state

def askCmd(command):
    # asks the user for a value, given a variable name (useful for scripting)
    if (len(command) == 0):
        errorMsg("ask", "no variable name was given")
        return

    var = command.pop(0) # takes variable name
    input_phrase = ""

    for word in command: # assembles input phrase with the other arguments
        input_phrase += word + " "

    value = input(input_phrase + f"[{var}]: ")

    if (value == ""): value = "0"

    return letCmd([var, "be", value])

def calcCmd(command, man_assign=True):
    if (man_var in variables):
        result = calculate(command)
        if (result is None): return
        elif (man_assign is False): print(result)
        else: variables[man_var] = result
    else: # gives an error
        errorMsg("calc", f"'{man_var}' is not a valid variable (man)")
        return
    return

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

    for word in range(len(command)):
        if (command[word] == "math.pi"): # replaces math.py variables
            command[word] = str(math.pi)
        elif (command[word] == "math.e"):
            command[word] = str(math.e)
        elif (command[word] in variables): # replaces long-name variables with their values
            try:
                command[word] = str(
                    calculate(
                        list(
                            str(
                                variables.get(command[word])
                                )
                            )
                        )
                    ).strip()
            except RecursionError as error: # when a lazy var is assigned to itself
                errorMsg("calc", "cannot calculate a variable with self assignment")
                print(error)
                return None
            #if (type(command[i]) == list):
            #    if (len(command) == 1): command[i] = command[i][0] # if item is a list with one element, takes first
            #    else:
            #        errorMsg("calc", "cannot multiply for an array")
            if (command[word] is None): return None # in case of calculate() error
            command[word] = str(command[word])

    command = "".join(str(word) for word in command) # concatenates command back into a string
    #//print(command)
    equation = ""
    for char in command:
        if (char.isalpha() and not char in operators):
            errorMsg("calc", f"{char} symbol / variable name ambiguity")
            return None
        else:
            #//print(i)
            equation += char

    #//print(equation)
    #equation = "".join(str(j) for j in equation) # concatenates equation back into a string
    #equation = equation.format_map(variables) # replaces variables with their values
    equation = equation.strip(" ") # strips whitespaces from equation

    if (equation == ""): equation = "0" # user input '=' results 0

    try:
        #//print(equation)
        return eval(equation)
    except SyntaxError as error:
        errorMsg("calc", f"cannot understand operation. \n{error}")
        return None
    except TypeError as error:
        errorMsg("calc", f"{error}")
        return None

def CLI():
    # command line function
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

def clsCmd(command):
    # clears console screen
    os.system("cls" if os.name=="nt" else "clear") # clears console screen
    print(f"### Welcome to chalk v{VERSION} ###\ntype 'help' for a list of commands")
    return

def cmdParser(command):
    # parses input commands
    command = command.split() # splits command given into a list

    if (command[0][0] == "="): # calc chortcut
        command[0] = command[0].lstrip("=") # strips "=" from command beginning
        return calcCmd(command)
    elif (command[0][0] == "?"): # calc without assign to man_var
        command[0] = command[0].lstrip("?") # strips "?" from command beginning
        return calcCmd(command, False)

    operator = command.pop(0) # sets operator var to the first keyword

    try:
        return globals()[operator + "Cmd"](command)
    except KeyError as error:
        errorMsg("cmdParser", f"command '{operator}' does not exist")
        print(error)
        return

def delCmd(command):
    deleted_variables = "variables deleted: "

    if (len(command) == 0): # if no argument is given
        errorMsg("del", "no variable specified")
        return
    if (len(command) == 1 and command[0] == "*"): # deletes all variables
        command.pop()
        for var in variables:
            if (var != "ans"):
                command.append(var)
    for var in command:
        if (var == man_var): print(manCmd([])) # if the variable was manipulated, man_var goes back to ans
        if (var in variables and var != "ans"):
            variables.pop(var) # removes variables
            deleted_variables += var + " "
        elif (var == "ans"): errorMsg("del", "cannot delete 'ans' variable")
        else: errorMsg("del", f"{var} is not an assigned variable")

    return deleted_variables

def errorMsg(module, message):
    # prints error messages
    print(f"<!> {module} error: {message}")
    return

def exitCmd(command):
    #closes chalk by setting "state" to False

    if (len(command) != 0):
        if (command[0] == "-s"): # saves variables to a file
            year, month, day, hour, min = map(int, time.strftime("%Y %m %d %H %M").split())
            saveCmd([f"./variables/{year}-{month}-{day}_{hour}-{min} -f"])

    global state
    state = False
    return "bye"

def helpCmd(command):
    # calls printHelp() with the chosen helpfile
    if (len(command) == 0): # prints the main help page (no argument given)
        with open("./docs/help/help") as helpfile:
            printHelp(helpfile)
        return
    command = command[0] # first argument is <command> help

    if (command == "me"): # :)
        print("oh no")
        return
    elif (command == "help"):
        print("help *<command>")
        print("\tprints the main help page or a specific <command> help page.")
        return

    try:
        if (command == "del"):
            with open("./docs/help/del") as helpfile:
                printHelp(helpfile)
            return
        elif (command == "exit"):
            with open("./docs/help/exit") as helpfile:
                printHelp(helpfile)
            return
        elif (command == "let"):
            with open("./docs/help/let") as helpfile:
                printHelp(helpfile)
            return
        elif (command == "load"):
            with open("./docs/help/load") as helpfile:
                printHelp(helpfile)
            return
        elif (command == "man"):
            with open("./docs/help/man") as helpfile:
                printHelp(helpfile)
            return
        elif (command == "run"):
            with open("./docs/help/run") as helpfile:
                printHelp(helpfile)
            return
        elif (command == "save"):
            with open("./docs/help/save") as helpfile:
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
        else:
            errorMsg("help", f"'{command}' help does not exist")
            return
    except FileNotFoundError as error:
        errorMsg("help", "help file not found, ./docs/help/ folder may be missing")
        print(error)
        return

def letCmd(command):
    # assigns new variables, without overwriting
    if (len(command) == 0): # if no variable is given, calls setCmd() to assign a new one
        return setCmd(command)

    for word in command:
        if (
            "=" in word and
            len(word) > 1
        ):
            spaced_equals = word.replace("=", " = ")
            spaced_equals = spaced_equals.split()
            equals_pos = command.index(word)
            command[equals_pos : equals_pos + 1] = spaced_equals

    var = command[0]

    if (var in variables):
        errorMsg("let", f"variable {var} is already set to {variables.get(var)}")
        return
    else:
        return setCmd(command)

def loadCmd(command):
    # loads variables from file
    if (len(command) == 0):
        errorMsg("load", "no filename was given")
        return

    vars_to_load = []
    force_set = False
    loaded_vars = "loaded variables: "

    filename = command.pop(0) # takes first argument as filename

    for word in command:
        if (word == "-s" or word == "-f"):
            command.remove(word)
            force_set = True

    try:
        with open(filename) as file:
            if (file.readline() != "variable, value\n"): # if first line is different
                errorMsg("load", f"'{filename}' is not a chalk variables csv file. Missing 'variable, value' header")
                return
            for line in file:
                var = line.strip().split(", ")
                vars_to_load.append(var)
    except FileNotFoundError as error:
        errorMsg("load", f"'{filename}' not found")
        print(error)
        return

    if (force_set is True):
        for var in vars_to_load:
            loaded_vars += var[0] + " "
            setCmd([var[0], "to", var[1]])
        loaded_vars += "('set' forced)"
    else:
        for var in vars_to_load:
            loaded_vars += var[0] + " "
            letCmd([var[0], "be", var[1]])

    return loaded_vars

def manCmd(command):
    # selects the variable for manipulation
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

def printHelp(helpfile):
    # prints each line of helpfile, formatting the variables
    for line in helpfile:
        print(line.rstrip().format(
            VERSION = VERSION,
            ))
    return

def saveCmd(command):
    # saves variables to file
    if (len(command) == 0):
        print("save warning: no filename was given, current date and time will be used")
        year, month, day, hour, min = map(int, time.strftime("%Y %m %d %H %M").split())
        command = [f"./variables/{year}-{month}-{day}_{hour}-{min}"]

    vars_to_save = []
    delete_vars = False
    force_overwrite = False
    saved_vars = "written variables: "

    filename = command.pop(0) # takes first argument as filename
    filename += ".csv"

    for word in command: # check if vars should be deleted and/or file overwritten
        if (word == "-d"):
            command.remove(word)
            delete_vars = True
        if (word == "-f"):
            command.remove(word)
            force_overwrite = True

    if (len(command) == 0): # check if all vars should be saved
        for var in variables:
            vars_to_save.append(var)
            saved_vars += var + " "
    else:
        for var in command: # appends all vars to be saved
            if (var in variables):
                vars_to_save.append(var)
                saved_vars += var + " "
            else: errorMsg("del", f"{var} is not an assigned variable")

    try:
        write_header = False
        with open(filename) as file: # check if file exists
            if (force_overwrite is True): # continues if -f
                errorMsg("save", f"'{filename}' already exists, data will be appended")
                if (file.readline() != "variable, value\n"): # if first line is different
                    errorMsg("save", f"'{filename}' is not a chalk variables csv file")
                    write_header = True
            else: # error and stops if not -f
                errorMsg("save", f"'{filename}' already exists, save aborted")
                return
        with open(filename, "a+") as file: # reopens file to append
            if (write_header is True): # writes header if not present already
                file.write("variable, value\n")
            for var in vars_to_save:
                if (type(variables.get(var)) != str): # if value is string, adds "&" for lazy assignments
                    file.write(f"{var}, {variables.get(var)}\n")
                else:
                    file.write(f"{var}, &{variables.get(var)}\n")
    except FileNotFoundError: # creates file if it doesn't exist
        with open(filename, "x") as file:
            file.write("variable, value\n")
            for var in vars_to_save:
                if (type(variables.get(var)) != str): # if value is string, adds "&" for lazy assignments
                    file.write(f"{var}, {variables.get(var)}\n")
                else:
                    file.write(f"{var}, &{variables.get(var)}\n")

    if (delete_vars is True): # deletes variables if requested
        saved_vars += "(and deleted)"
        delCmd(vars_to_save)

    return saved_vars

def sayCmd(command):
    # prints on screen all the arguments given
    echo = ""

    for word in command:
        if (word[0] == "&"): # evaluates that variable
            echo += str(
                calculate(
                    [word.lstrip("&")]
                    )
                ) + " "
        else:
            echo += word + " "

    return echo

def setCmd(command):
    # assigns variables overwriting
    if (len(command) == 0): # if no variable is given, a free one is assigned
        command.append(free_vars.pop())

    for word in command:
        if (
            "=" in word and
            len(word) > 1
        ):
            spaced_equals = word.replace("=", " = ")
            spaced_equals = spaced_equals.split()
            equals_pos = command.index(word)
            command[equals_pos : equals_pos + 1] = spaced_equals

    var = command[0]
    for char in var:
        if (not char.isalpha()):
            errorMsg("let/set", f"variable names cannot contain digits or symbols '{char}'")
            return

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
            for char in range(1, len(command)):
                if (command[char] != ""):
                    value += str(command[char]) + " "
                #value = " ".join(command[i])
            value = value.rstrip()
            variables[var] = value
            return f"(lazy) {var} = {value}"
        value = calculate(command[1 : None])
        if (value is None):
            errorMsg("let/set", "cannot assign empty variable")
            return

    if (var in free_vars): # removes var from free_vars when it is assigned
        free_vars.remove(var)

    variables[var] = value
    return f"{var} = {value}"

def varCmd(command):
    # prints variables values
    vars_to_print = []
    alph_order = False

    for word in command:
        if (word == "-a"):
            command.remove(word)
            alph_order = True

    if (len(command) == 0): # no arguments given, appends all variables
        for var in variables:
            vars_to_print.append(var)
    else: # var arguments are given and appended
        for var in command:
            vars_to_print.append(var)

    if (alph_order is True): vars_to_print = sorted(vars_to_print)

    for var in vars_to_print:
        if (var not in variables): print(f"{var} is not an assigned variable")
        else: print(f"\t{var}\t=\t{variables.get(var)}")

    return

def varManUpd():
    # updates the manipulated var string
    global man_var
    global man_value

    if (man_var in variables):
        man_value = variables.get(man_var)
    else:
        errorMsg("varManUpd", f"CRITICAL the variable {man_var} doesn't exist")
        return

    return

def runCmd(command):
    # runs given script file
    if (len(command) == 0):
        errorMsg("run", "no script file was given")
        return

    filename = command[0]
    commands = []

    try:
        with open(filename) as script:
            for line in script:
                commands.append(line.strip())
    except FileNotFoundError as error:
        errorMsg("run", "script file not found")
        print(error)
        return

    for line in commands:
        if (line[-1] != ";"): # doesn't print commands ending with ";"
            output = cmdParser(line)
            if (output is not None):
                print(output)
        else: cmdParser(line)

if __name__ == "__main__":
    CLI()