from os import system, name
from time import strftime, time
from traceback import print_exc
import math
import numpy as np

VERSION = "1.1.2-beta"

free_vars = set((
	"a0", "b0", "c0", "d0", "e0", "f0", "g0", "h0", "i0", "j0", "k0", "l0", "m0", "n0", "o0", "p0", "q0", "r0", "s0", "t0", "u0", "v0", "w0", "x0", "y0", "z0",
	"a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1", "i1", "j1", "k1", "l1", "m1", "n1", "o1", "p1", "q1", "r1", "s1", "t1", "u1", "v1", "w1", "x1", "y1", "z1",
	"a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2", "i2", "j2", "k2", "l2", "m2", "n2", "o2", "p2", "q2", "r2", "s2", "t2", "u2", "v2", "w2", "x2", "y2", "z2",
	"a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3", "i3", "j3", "k3", "l3", "m3", "n3", "o3", "p3", "q3", "r3", "s3", "t3", "u3", "v3", "w3", "x3", "y3", "z3",
	"a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4", "i4", "j4", "k4", "l4", "m4", "n4", "o4", "p4", "q4", "r4", "s4", "t4", "u4", "v4", "w4", "x4", "y4", "z4",
	"a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5", "i5", "j5", "k5", "l5", "m5", "n5", "o5", "p5", "q5", "r5", "s5", "t5", "u5", "v5", "w5", "x5", "y5", "z5",
	"a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6", "i6", "j6", "k6", "l6", "m6", "n6", "o6", "p6", "q6", "r6", "s6", "t6", "u6", "v6", "w6", "x6", "y6", "z6",
	"a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7", "i7", "j7", "k7", "l7", "m7", "n7", "o7", "p7", "q7", "r7", "s7", "t7", "u7", "v7", "w7", "x7", "y7", "z7",
	"a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8", "i8", "j8", "k8", "l8", "m8", "n8", "o8", "p8", "q8", "r8", "s8", "t8", "u8", "v8", "w8", "x8", "y8", "z8",
	"a9", "b9", "c9", "d9", "e9", "f9", "g9", "h9", "i9", "j9", "k9", "l9", "m9", "n9", "o9", "p9", "q9", "r9", "s9", "t9", "u9", "v9", "w9", "x9", "y9", "z9"
))
used_vars = set()
variables = dict([
	("ans", 0)
])
aliases = dict()

man_var = "ans" # currently manipulated variable
man_value = "" # currently manipulated variable value

state = True # CLI "on" state
script_interrupted = False # script interrupt

tic_toc_time = time()

def askCmd(command):
	"""asks the user for a value, given a variable name (useful for scripting)"""
	global script_interrupted

	if (len(command) == 0):
		errorMsg("ask", "no variable name was given")
		return

	var = command.pop(0) # takes variable name
	if (var[0] == "@"): # checks for aliases
		var = aliases[var.lstrip("@")]

	input_phrase = ""

	for word in command: # assembles input phrase with the other arguments
		input_phrase += word + " "

	try:
		value = input(input_phrase + f"[{var}]: ")
	except KeyboardInterrupt:
		script_interrupted = True
		return

	if (value == ""): value = "0"

	return setCmd([var, "be", value])

def calcCmd(command, man_assign=True):
	"""calc command"""
	if (man_var in variables):
		result = calculate(command) # calculates result
		#//print(result) # debugging
		if (result is None): return
		elif (man_assign is False): print(result) # if called with "?" only prints
		else: # otherwise assigns
			variables["old"] = variables[man_var] # saving the old result
			variables[man_var] = result
	else: # gives an error
		errorMsg("calc", f"'{man_var}' is not a valid variable (man)")
		return
	return

def calculate(command):
	"""evaluates calculations"""
	operators = "+-*(),; /[]%!:#^'" # allowed operators

	command = "".join(command) # turns command into a string
	command = command.strip() # removes whitespaces

	if (len(command) == 0): return 0 # if input is empty, returns 0

	equation = [] # empty equation list
	word = "" # empty word
	for char_pos in range(len(command)):
		if (command[char_pos] in operators): # if char is an operator
			equation.append(word) # appends previous word
			equation.append(command[char_pos]) # appends operator
			word = "" # starts new word
		else: word += command[char_pos] # else adds char to word
	equation.append(word) # appends last word to equation

	#//print(equation) # debugging

	for word in range(len(equation)):
		# need to for-loop on pos because python sucks big dick
		# and would not replace strings ¯\_(^^)_/¯
		if (len(equation[word]) > 0):
			if (equation[word][0] == "@"): # checks for aliases
				equation[word] = equation[word].lstrip("@")
				if (equation[word] in aliases):
					equation[word] = aliases[equation[word]]
				else:
					errorMsg("calc", "alias not found")
					return

		if (len(equation[word]) == 1): # checks for custom operators
			if (equation[word] == ":"): # square root symbol
				equation[word] = "math.sqrt"
			elif (equation[word] == "!"): # factorial symbol
				equation[word] = "math.factorial"
			elif (equation[word] == "#"): # array symbol
				equation[word] = "np.array"
			elif (equation[word] == "^"): # scientific notation symbol
				equation[word] = "*10**"
			elif (equation[word] == "'"): # scientific notation symbol
				equation[word] = "np.transpose"
			elif (equation[word] == "%"): # scientific notation symbol
				equation[word] = "*0.01*"

		if (equation[word] in variables): # replaces variables with their values
			try:
				if ("numpy" in str(type(variables.get(equation[word])))):
					equation[word] = "np.array(" + str(
						variables.get(equation[word]).tolist()
					) + ")"
				else:
					equation[word] = str(
						calculate( # calc is necessary if var is lazy-assigned
							list( # calc accepts lists of strings
								str(
									variables.get(equation[word])
								)
							)
						)
					).strip()
			except RecursionError: # when a lazy var is assigned to itself
				errorMsg("calc", "cannot calculate a variable with self assignment")
				print_exc()
				return None
			if (equation[word] is None): return None # in case of calculate() error

		#//print("word: " + equation[word]) # debugging

	equation = "".join(str(word) for word in equation) # concatenates equation back into a string

	#//print("eq: " + equation) # debugging

	if (equation == ""): equation = "0" # user input '=' results 0

	try:
		return eval(equation)
	except SyntaxError:
		errorMsg("calc", f"syntax error")
		print_exc()
		return None
	except TypeError:
		errorMsg("calc", "type error")
		print_exc()
		return None
	except NameError:
		errorMsg("calc", "name error")
		print_exc()
		return None
	except ValueError:
		errorMsg("calc", "value error")
		print_exc()
		return None
	except AttributeError:
		errorMsg("calc", "attribute error")
		print_exc()
		return None
	except ZeroDivisionError:
		errorMsg("calc", "zero division error")
		print_exc()
		return None

def CLI():
	"""command line function"""
	print(f"### Welcome to chalk v{VERSION} ###\ntype 'help' for a list of commands") # welcome message

	while (state is True):
		manVarUpd()
		try:
			command = input(f"\n================\n{man_value} <{man_var}> $ ") # command input
		except KeyboardInterrupt:
			print(exitCmd([]))
			return
		if (len(command) == 0 or command.split() == []): errorMsg("CLI", "no command was given")
		else:
			if (command[-1] == ";"): # if command ends with ';' execute command without printing
				command = command.rstrip(";")
				cmdParser(command)
			else: # otherwise print command result
				result = cmdParser(command)
				if (result != None):
					print(result)

	return

def clsCmd(command):
	"""clears console screen"""
	system("cls" if name=="nt" else "clear") # clears console screen
	print(f"### Welcome to chalk v{VERSION} ###\ntype 'help' for a list of commands")
	return

def cmdParser(command):
	"""parses input commands"""
	command = command.split() # splits command given into a list

	if (command[0][0] == "="): # calc chortcut
		command[0] = command[0].lstrip("=") # strips "=" from command beginning
		return calcCmd(command)
	elif (command[0][0] == "?"): # calc without assign to man_var
		command[0] = command[0].lstrip("?") # strips "?" from command beginning
		return calcCmd(command, False)
	elif (command[0][0] == "+" and command[0][1] == "="): # calc with quick operation
		command[0] = command[0].lstrip("+=") # strips quick operand from command beginning
		command[0] = man_var + "+" + command[0] # adds man_var and operand
		return calcCmd(command)
	elif (command[0][0] == "-" and command[0][1] == "="):
		command[0] = command[0].lstrip("-=")
		command[0] = man_var + "-" + command[0]
		return calcCmd(command)
	elif (command[0][0] == "*" and command[0][1] == "="):
		command[0] = command[0].lstrip("*=")
		command[0] = man_var + "*" + command[0]
		return calcCmd(command)
	elif (command[0][0] == "/" and command[0][1] == "="):
		command[0] = command[0].lstrip("/=")
		command[0] = man_var + "/" + command[0]
		return calcCmd(command)

	operator = command.pop(0) # sets operator var to the first keyword

	try:
		return globals()[operator + "Cmd"](command)
	except KeyError:
		errorMsg("cmdParser", f"command '{operator}' exception")
		print_exc()
		return

def defCmd(command):
	"""assigns aliases"""
	if (len(command) == 0): # prints the aliases table
		aliases_to_print = ""
		for alias in aliases:
			aliases_to_print += "@" + alias + "\t=\t" + aliases[alias] + "\n"
		return aliases_to_print

	aliases_created = ""

	for var in command:
		if(not any(char.isalpha() for char in var)): # check there's at least one letter
			errorMsg("def", "cannot assign aliases that don't contain letters")
			return aliases_created
		for char in var: # check it doesn't contain symbols
			if (not char.isalnum()):
				errorMsg("def", f"aliases must be alphanumeric - '{char}'")
				return
		new_var = letCmd([]).split()[0]

		aliases[var] = new_var
		aliases_created += "@" + var + "\t=\t" + new_var + "\n"
	return aliases_created

def delCmd(command):
	"""deletes variables"""
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
		if (var[0] == "@"): # checks for aliases
			var = aliases[var.lstrip("@")]
		if (var == man_var): print(manCmd([])) # if the variable was manipulated, man_var goes back to ans
		if (var in variables and var != "ans"):
			variables.pop(var) # removes variables
			if (var in used_vars):
				used_vars.remove(var) # removes from used_vars
				free_vars.add(var) # puts in free_vars
			deleted_variables += var + " "
		elif (var == "ans"): errorMsg("del", "cannot delete 'ans' variable")
		else: errorMsg("del", f"{var} is not an assigned variable")

	return deleted_variables

def errorMsg(module, message):
	"""prints error messages"""
	print(f"<!> {module} error: {message}")
	return

def exitCmd(command):
	"""closes chalk by setting "state" to False"""

	if (len(command) != 0):
		if (command[0] == "-s"): # saves variables to a file
			year, month, day, hour, min = map(int, strftime("%Y %m %d %H %M").split())
			saveCmd([f"./variables/{year}-{month}-{day}_{hour}-{min} -f"])

	global state
	state = False
	return "bye"

def helpCmd(command):
	"""calls printHelp() with the chosen helpfile"""
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
		if (command == "ask"):
			with open("./docs/help/ask") as helpfile:
				printHelp(helpfile)
			return
		elif (command == "calc"):
			with open("./docs/help/calc") as helpfile:
				printHelp(helpfile)
			return
		elif (command == "def"):
			with open("./docs/help/def") as helpfile:
				printHelp(helpfile)
			return
		elif (command == "del"):
			with open("./docs/help/del") as helpfile:
				printHelp(helpfile)
			return
		elif (command == "exit"):
			with open("./docs/help/exit") as helpfile:
				printHelp(helpfile)
			return
		elif (command == "foreach"):
			with open("./docs/help/foreach") as helpfile:
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
		elif (command == "say"):
			with open("./docs/help/say") as helpfile:
				printHelp(helpfile)
			return
		elif (command == "set"):
			with open("./docs/help/set") as helpfile:
				printHelp(helpfile)
			return
		elif (command == "tic"):
			with open("./docs/help/tic") as helpfile:
				printHelp(helpfile)
			return
		elif (command == "toc"):
			with open("./docs/help/toc") as helpfile:
				printHelp(helpfile)
			return
		elif (command == "type"):
			with open("./docs/help/type") as helpfile:
				printHelp(helpfile)
			return
		elif (command == "var"):
			with open("./docs/help/var") as helpfile:
				printHelp(helpfile)
			return
		else:
			errorMsg("help", f"'{command}' help does not exist")
			return
	except FileNotFoundError:
		errorMsg("help", "help file not found, ./docs/help/ folder may be missing")
		print_exc()
		return

def letCmd(command):
	"""assigns new variables, without overwriting"""
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
	if (var[0] == "@"): # checks for aliases
		var = aliases[var.lstrip("@")]

	if (var in variables):
		errorMsg("let", f"variable {var} is already set to {variables.get(var)}")
		return
	else:
		return setCmd(command)

def loadCmd(command):
	"""loads variables from file"""
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
				var = line.strip().split(", ", 1)
				vars_to_load.append(var)
	except FileNotFoundError:
		errorMsg("load", f"'{filename}' not found")
		print_exc()
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
	"""selects the variable for manipulation"""
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

def manVarUpd():
	"""updates the manipulated var string"""
	global man_var
	global man_value

	if (man_var in variables):
		man_value = variables.get(man_var)
		#//print(man_value) # debugging
	else:
		errorMsg("varManUpd", f"CRITICAL the variable {man_var} doesn't exist")
		return

	return

def printHelp(helpfile):
	"""prints each line of helpfile, formatting the variables"""
	for line in helpfile:
		print(line.rstrip().format(
			VERSION = VERSION,
			))
	return

def saveCmd(command):
	"""saves variables to file"""
	if (len(command) == 0):
		print("save warning: no filename was given, current date and time will be used")
		year, month, day, hour, min = map(int, strftime("%Y %m %d %H %M").split())
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
				if (type(variables.get(var)) == str): # if value is string, adds "&" for lazy assignments
					file.write(f"{var}, &{variables.get(var)}\n")
				elif ("numpy" in str(type(variables.get(var)))): # if value is numpy array, writes "header"
					file.write(f"{var}, np.array({str(variables.get(var).tolist())})\n")
				else:
					file.write(f"{var}, {variables.get(var)}\n")
	except FileNotFoundError: # creates file if it doesn't exist
		try:
			with open(filename, "x") as file:
				file.write("variable, value\n")
				for var in vars_to_save:
					if (type(variables.get(var)) == str): # if value is string, adds "&" for lazy assignments
						file.write(f"{var}, &{variables.get(var)}\n")
					elif ("numpy" in str(type(variables.get(var)))): # if value is numpy array, writes "header"
						file.write(f"{var}, np.array({str(variables.get(var).tolist())})\n")
					else:
						file.write(f"{var}, {variables.get(var)}\n")
		except FileNotFoundError: # if file is actually not existing
			errorMsg("save", f"'{filename}' can't be written to, check the path; save aborted")
			return

	if (delete_vars is True): # deletes variables if requested
		saved_vars += "(and deleted)"
		delCmd(vars_to_save)

	return saved_vars

def sayCmd(command):
	"""prints on screen all the arguments given"""
	echo = ""

	for word in command:
		if (word[0] == "&"): # evaluates that variable
			echo += str(
				calculate(
					[word.lstrip("&")]
					)
				) + " "
		elif (word[0] == "@"): # evaluates that alias
			echo += aliases[word.lstrip("@")] + " "
		else:
			echo += word + " "

	return echo

def setCmd(command):
	"""assigns variables overwriting"""
	if (len(command) == 0): # if no variable is given, a free one is assigned
		command.append(free_vars.pop())
		used_vars.add(command[0]) # puts var into used_vars


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
	if (var[0] == "@"): # checks for aliases
		var = aliases[var.lstrip("@")]

	if(not any(char.isalpha() for char in var)): # check there's at least one letter
		errorMsg("let/set", "variable names must contain at least one letter")
		return
	for char in var: # check it doesn't contain symbols
		if (not char.isalnum()):
			errorMsg("let/set", f"variable names must be alphanumeric - '{char}'")
			return

	if (len(command) == 1): # if no value is given, man_value is taken
		value = man_value
	elif (command[1].lower() != "be" and command[1].lower() != "=" and command[1].lower() != "to"):
		errorMsg("let/set", "missing 'be' / '=' / 'to' keyword")
		return
	else:
		command.pop(1)
		try:
			if (command[1][0] == "&"): # lazy assignment
				value = ""
				command[1] = command[1].lstrip("&")
				for word in range(1, len(command)):
					if (command[word] != ""):
						value += str(command[word]) + " "
					#value = " ".join(command[i])
				value = value.rstrip()
				variables[var] = value
				return f"(lazy) {var} = {value}"
			value = calculate(command[1 : None])
		except:
			value = None
		if (value is None):
			errorMsg("let/set", "cannot assign empty variable")
			return

	if (var in free_vars):
		free_vars.remove(var) # removes var from free_vars
		used_vars.add(var) # puts it into used_vars

	variables[var] = value

	print_value = ""
	for char in str(value):
		if (char == "\n"):
			print_value += "\n\t\t"
		else: print_value += char

	return f"{var}\t=\t{print_value}"

def ticCmd(command):
	global tic_toc_time
	tic_toc_time = time()
	return

def tocCmd(command):
	global tic_toc_time
	return "time elapsed: " + str(time() - tic_toc_time)

def varCmd(command):
	"""prints variables values"""
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
			if (var[0] == "@"): # checks for aliases
				var = aliases[var.lstrip("@")]
			vars_to_print.append(var)

	if (alph_order is True): vars_to_print = sorted(vars_to_print)

	for var in vars_to_print:
		if (var not in variables): print(f"{var} is not an assigned variable")
		else:
			value = str(variables.get(var))
			print_value = ""
			for char in value:
				if (char == "\n"):
					print_value += "\n\t\t\t"
				else: print_value += char
			print(f"\t{var}\t=\t{print_value}")

	return

def runCmd(command):
	"""runs given script file"""
	global script_interrupted
	script_interrupted = False

	if (len(command) == 0):
		errorMsg("run", "no script file was given")
		return

	filename = command[0]
	commands = []

	try:
		with open(filename) as script:
			for line in script:
				if (line[0] != "#" and len(line.strip()) != 0): # ignores comments and empty lines
					commands.append(line.strip())
	except FileNotFoundError:
		errorMsg("run", "script file not found")
		print_exc()
		return

	for line in commands:
		if (script_interrupted is False):
			manVarUpd()
			if (line[-1] != ";"): # check if command ends with ";"
				output = cmdParser(line)
				if (output is not None):
					print(output)
			else: cmdParser(line.rstrip(";"))
		else:
			errorMsg("run", "script interrupted by user command")
			return

	return

def typeCmd(command):
	"""prints variables types"""
	vars_to_print = []

	if (len(command) == 0): # no arguments given, appends all variables
		for var in variables:
			vars_to_print.append(var)
	else: # var arguments are given and appended
		for var in command:
			if (var[0] == "@"): # checks for aliases
				var = aliases[var.lstrip("@")]
			vars_to_print.append(var)

	for var in vars_to_print:
		if (var not in variables): print(f"{var} is not an assigned variable")
		else:
			var_type = str(type(variables[var])).lstrip("<class ").rstrip(">")
			if (var_type[1] in "aeiou"): # uses "an" for types starting with vocal
				print(f"\t{var}\tis an\t{var_type}")
			else: # otherwise "a" for types starting with consonant
				print(f"\t{var}\tis a\t{var_type}")

	return

def foreachCmd(command):
	"""executes calculation to all variables given"""
	operators = "+-*/" # allowed operators
	vars_to_set = []

	if (len(command) == 0): # if no argument is given
		errorMsg("foreach", "no arguments given")
		return

	arg_is_var = True
	calculation = ""
	for arg in command:
		if (arg_is_var):
			if (arg[0] in operators):
				arg_is_var = False
				calculation += arg
				continue
			if (arg[0] == "@"): # checks for aliases
				arg = aliases[arg.lstrip("@")]
			vars_to_set.append(arg)
		else:
			calculation += arg

	if (len(vars_to_set) == 0):
		errorMsg("foreach", "no variable was given")
		return

	for var in vars_to_set:
		if var not in variables:
			errorMsg("foreach", f"variable {var} does not exist")
			vars_to_set.remove(var)

	if (arg_is_var or len(calculation) == 0):
		errorMsg("foreach", "no calculation was given")
		return
	elif (calculation[0] in operators):
		operator = calculation[0]
		calculation = calculation[1:]
	else:
		errorMsg("foreach", "no operator found in calculation")
		return

	for var in vars_to_set:
		value = calculate(f"{var} {operator} {calculation}")
		print(setCmd([var, "be", str(value)]))

	return

if __name__ == "__main__":
	CLI()
