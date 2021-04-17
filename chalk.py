import math

VERSION = "0dev"

const_vars = set(("e", "pi", "ans"))
e = math.e
pi = math.pi
ans = 0

free_vars = set(("", "b", "c", "d", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "W", "X", "Y", "Z"))
used_vars = set(("a"))

def letOp(var, value):
    if (var in used_vars): return "variable is already set"
    else:
        return setOp(var, value)

def setOp(var, value):
    used_vars.add(var)
    exec(f"{var} = {value}")
    return 

def cmdParser(command):
    command = command.split()
    operator = command[0]
    if (operator == "let"):
        print(letOp(command[1], command[3]))
    elif (operator == "set"):
        print(setOp(command[1], command[3]))
    elif (operator == "vars"):
        print(f"system variables: {const_vars}\nused variables: {used_vars}")

def CLI():
    print(f"### Welcome to chalk.py v{VERSION} ###\ntype 'help' for a list of commands") # welcome message

    command = ""
    while (command != "exit"):
        try:
            command = input("~> ") # command input
            cmdParser(command)
        except IndexError as error:
            print(f"{error}")
    print("bye")

if __name__ == "__main__":
    CLI()