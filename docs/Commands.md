# chalk documentation: Commands

## Table of contents:

1. [Calculations](#calculations)
2. [Variables](#variables)
	1. [Assignment](#assignment)
	2. [Display](#print-variables)
	3. [Manipulation](#manipulation)
	4. [Deletion](#deletion)
	5. [Saving and loading](#saving-and-loading)
3. [Scripting](#scripting)
4. [Useful commands](#useful-commands)

## Calculations

The 'calc' command solves arithmetic expressions.
You can also call it more quickly with '='.
	
	calc 5+4

	=5+4
will store '9' in the currently manipulated variable.

You can also get results without storing the value, by calling 'calc' with '?':

	?5+4
will print the result '9' without assigning it.

You can also use variables and math (python module) constants in your calculations.

##### Note: within expressions, you must separate variable names with whitespaces, to avoid ambiguity: for instance, '1+ a + b \*8+6'.

## Variables

These two commands allow you to store variables.

### Assignment

#### let

Allows you to create a new variable, without replacing an existing value.

	let <var> be <value>
stores a new variable \<var> with the value \<value>. If it exists already, you will get an error.

	let <var>
stores a new variable \<var> with the currently manipulated value.

	let
stores a new variable, with a random one-letter name that isn't being used, with the currently manipulated value.


#### set

Allows you to create a new variable, overwriting an exising one with the same name if it exists.

	set <var> to <value>
stores a new variable \<var> with the value \<value>.

	set <var>
stores a new variable \<var> with the currently manipulated value.

	set
stores a new variable, with a random one-letter name that isn't being used, with the currently manipulated value.

#### Lazy assignment

You can assign expressions to variables, that will be evaluated when the variables are called, instead of when they're assigned.
To use lazy assignment, you can type '&' followed by your expression, which will be stored as a string as the value of that variable.

	let a be &5+ b
will result in:

	a = 5+ b

When the variable is used in calculations, the value will be solved in real time.

### Print variables

The 'var' command prints the list of currently stored variables.
By default, they're ordered chronologically; you can order them alphabetically by adding '-a'.

You can give as arguments the names of the variables you want to display, separated by whitespaces.

### Manipulation

Variable manipulation is a key feature of chalk which allows you to have a variable always-at-hand, to store all of your results.
Whenever you type a calculation (with the 'calc' command or its alias '='), the result is stored in the manipulated variable ('ans' by default).

The 'man' command lets you select the variable you want to manipulate. If you want to go back to 'ans', you can just type 'man' without any arguments.

### Deletion

The 'del' command lets you delete one or more variables.
If the currently manipulated variable is deleted, 'man' will automatically revert the manipulation to 'ans'.

Note that you can't delete the 'ans' variable, and remember that all variable deletions are permanent.

### Saving and loading

The 'save' command allows you to write variables to a file.
The file will be formatted as csv, as:

	variable, value
	a, 0
	b, 1
	c, &b +4

If no filename is given, the current date and time will be used.

You can choose to save only some variables, typing them as arguments.

Optional arguments:
'-d' deletes the variables after they've been saved
'-f' forces overwriting in case the filename already exists



The 'load' command is used to read variables from a csv file and store them in your current environment.
To avoid errors, it is best to only load variable files created by chalk.

The '-s' argument is used to force 'set' when importing, which will overwrite existing variables with conflicting names.

## Scripting

## Useful commands

- 'cls' clears the console screen.
- 'exit' closes chalk.
- 'help' displays the main help page; you can add the name of a command afterwards to print its specific help page.