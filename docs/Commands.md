# chalk documentation: Commands

## Table of contents:

1. [Syntax](#syntax)
2. [Calculations](#calculations)
	1. [`calc` command](#calc)
	2. [Additional operations](#additional-operations)
	3. [Algebra (tuples, vectors and matrices)](#algebra)
		1. [Indices and length](#indices-and-length)
		2. [Tuples](#tuples-and-lists)
		3. [Vectors (arrays)](#arrays)
3. [Variables](#variables)
	1. [Assignment](#assignment)
	2. [Printing](#print-variables)
	3. [Manipulation](#manipulation)
	4. [Deletion](#deletion)
	5. [Saving and loading](#saving-and-loading)
	6. [Types](#types)
4. [Scripting](#scripting)
	1. [`run` command](#the-run-command-allows-you-to-run-script-files-in-chalk)
	2. [`def` command and aliases](#def)
	3. [`ask` command](#ask)
	4. [`say` command](#say)
5. [Useful commands](#useful-commands)

## Syntax

To input commands in chalk, you simply type the command, followed by the arguments, all separated by ` ` whitespaces.
To learn more information about the specific syntax of each command, you can use `help`.
Some commands, such as `help`, do not require arguments, but can accept some.

Many commands will output the result of the actions after you've executed them: if you wish to hide the output of some particular commands, you simply add `;` to the end of the line; for instance:

	let a be 5;
will not print in the console the line

	a = 5

## Calculations

### calc

This command solves arithmetic expressions.
You can also call it more quickly with `=`.
	
	calc 5+4

	=5+4
will store `9` in the currently manipulated variable.

You can also get results without storing the value, by calling `calc` with `?`:

	?5+4
will print the result `9` without assigning it.

You can also use variables and `math` (python module) constants and functions in your calculations.

#### Quick operands

You can easily make additions, subtractions, multiplications and divisions to the manipulated variable with quick operands, by putting the desired operand before the `=` command.

For example:

	5 <ans> $ += 10
	15 <ans> $
and the same applies to arrays as well:

	[[4 2]
	 [8 6]] <ans> $ /=2

	[[2 1]
	 [4 3]] <ans> $

---
### Additional operations

Here's symbolic shortcuts for some operations you might frequently use:
- `^` scientific notation *(equivalent to `*10**`)*
- `:` square root *(equivalent to `math.sqrt`)*
- `!` factorial *(equivalent to `math.factorial`)*

In order to use these shortcuts, you must use parentheses to specify the arguments (except for `^`). For instance:

	=:(2)
calculates the square root of 2.

	=a^-11
calculates a*10**-11

---
### Algebra

Within chalk, you can make operations with variable types other than floats, like for instance tuples and vectors.

#### Indices and length

Both of these types can contain more than one value, and they can be accessed through indices.
Indices inside a tuple or an array, start from `0`, up to the length of the object - 1.

To access a value inside a tuple / array, type the index within `[ ]` square brackets; for example:

	$ let a be (1,2)
	a = (1, 2)
	$ let a0 be a[0]
	a0 = 1
To know the length of a tuple / array, you can use the operator `len`, giving the object (of which you want to know the length) within `( )` parentheses.

	$ ?len(a)
	2

#### Tuples and lists

Tuples are, in a way, lists of floats, which are "grouped" together in `( )` parentheses. They are useful to store in one variable multiple values, like coefficients, conjugate square roots, etc.

Operations like subtraction and division don't work with tuples, but other operands do:
- `+` adds items to the tuple; for instance: `(1, 2) + 3 ==> (1, 2, 3)` and `(1, 2) + (1, 4) ==> (1, 2, 1, 4)`.
- `*` multiplies the number of values inside the tuple; for example: `(1, 2) * 3 ==> (1, 2, 1, 2, 1, 2)`.

Most of other operations are not allowed, and will simply output an error.

Lists work a lot like tuples, and are denoted by `[ ]` square brackets. They behave in much of the same way, but their use is not recommended. For algebraic operations, arrays have many more features and should be used instead.

#### Arrays

Arrays are very useful algebraic tools: they're lists of values, within `[ ]` square brackets.

To create arrays, you can use the operator `#` *(equivalent to `np.array`)* with the notation `([])`, as follows:

	let a be #([1,2,3])
which will create an array `[1, 2, 3]`.

> Note: the `( )` parentheses denote the function of creating the array, whereas the `[ ]` square brackets denote the array of values.

This type of value is very powerful, and handled, on the backend, by the Python module `numpy`.
All of the operations and transformations available by numpy, are fully supported by chalk.

> Note: `numpy` has been imported as `np`, so all the module's operations and methods can be called with either name.

For more information on `numpy`:
- [official quickstart guide *(recommended)*](https://numpy.org/doc/stable/user/quickstart.html)
- [w3schools guide *(recommended)*](https://www.w3schools.com/python/numpy/numpy_intro.asp)
- [official manual](https://numpy.org/doc/stable/)
- [official reference](https://numpy.org/doc/stable/reference/)

#### Matrices

Matrices in `numpy` are handled as *arrays of arrays*, as in a collection of row- (or column-) vectors.
This way of storing matrices may seem counter-intuitive, but is actually really handy.

You can find more information in the `numpy` documentation.

## Variables

### Assignment

#### let

Allows you to create a new variable, without replacing an existing value.

	let <var> be <value>
stores a new variable `<var>` with the value `<value>`. If it exists already, you will get an error.

	let <var>
stores a new variable `<var>` with the currently manipulated value.

	let
stores a new variable, with a random one-letter name that isn't being used, with the currently manipulated value.

#### set

Allows you to create a new variable, overwriting an exising one with the same name if it exists.

	set <var> to <value>
stores a new variable `<var>` with the value `<value>`.

	set <var>
stores a new variable `<var>` with the currently manipulated value.

	set
stores a new variable, with a random one-letter name that isn't being used, with the currently manipulated value.

#### Lazy assignment

You can assign expressions to variables, that will be evaluated when the variables are called, instead of when they're assigned.
To use lazy assignment, you can type `&` followed by your expression, which will be stored as a string as the value of that variable.

	let a be &5+b
will result in:

	a = 5+b

When the variable is used in calculations, the value will be solved in real time.

---
### Print variables

The `var` command prints the list of currently stored variables.
By default, they're ordered chronologically; you can order them alphabetically by adding `-a`.

You can give as arguments the names of the variables you want to display, separated by ` ` whitespaces.

---
### Manipulation

Variable manipulation is a key feature of chalk which allows you to have a variable always-at-hand, to store all of your results.
Whenever you type a calculation (with the `calc` command or its alias `=`), the result is stored in the manipulated variable (`ans` by default).

The `man` command lets you select the variable you want to manipulate. If you want to go back to `ans`, you can just type `man` without any arguments.

---
### Deletion

The `del` command lets you delete one or more variables.
To delete all variables, simply type `del *`.

If the currently manipulated variable is deleted, `man` will automatically revert the manipulation to `ans`.
Note that you can't delete the `ans` variable, and remember that all variable deletions are permanent.

---
### Saving and loading

The `save` command allows you to write variables to a file.
The file will be formatted as csv, as:

	variable, value
	a, 0
	b, 1
	c, &b+4

If no filename is given, the current date and time will be used.

You can choose to save only some variables, typing them as arguments.

Optional arguments:
`-d` deletes the variables after they've been saved
`-f` forces overwriting in case the filename already exists



The `load` command is used to read variables from a csv file and store them in your current environment.
To avoid errors, it is best to only load variable files created by chalk.

The `-s` argument is used to force `set` when importing, which will overwrite existing variables with conflicting names.

### Types

Every variable has a type, which depends on the value stored inside.
The most common types will be:
- `'int'`
- `'float'`
- `'str'` *(string)*
- `'tuple'`
- `'np.ndarray'` *(array)*

To know which type one (or more) variable is, you can use the command `type`.

> Note: string types appear every time you lazy-assign a variable; the string **will be evaluated by calc** whenever that variable is called.

## Scripting

chalk allows you to run scripts (recipes, lists of commands) to do calculations: they are useful to save formulas and expressions related to variables, as well as being able to share them with other users.

##### The `run` command allows you to run script files in chalk.

---
You can create a scipt in any text editor, typing for each text line, a chalk command, as you would in the CLI.

> It is good practice to put ';' at the end of commands of which you do **not** want the result printed.

For scripting purpose, there exist some commands that will make it possilbe to easily create functions and calculators.

---
### def

This command lets you to give temporary names to variables, called aliases, that can be parsed by preceding them with `@`.
This feature is especially useful in scripting, as it allows for the use of the same names, without overwriting any of the user variables.
For instance:

	def radius area depth
creates three new variables, with *real* names assigned by the `let` command, having as aliases `radius`, `area` and `depth` respectively.
Let's say that the names given by `let` were `h0`, `t4` and `g3`: `def` will output

	@radius   =    h0
	@area     =    t4
	@depth    =    g3
and from then on, at every occurrence of the alias `@area`, the variable `t4` will be called.

---
### ask

This command allows you to ask for a variable value, and automatically assign it to a name, that can later be used for calculations.
The syntax is very simple:

	ask <var> *<phrase>

where `<var>` is the variable name, and `<phrase>` is the text that will be presented to the user when the value is asked.
By default, if no value is entered, `0` will be taken.

It uses the `set` command for assignment.

---
### say

This command prints on the CLI the phrase that is given as argument.

It allows to print variable values, preceded by `&`.
For instance, given a variable `a` of value `5`:

	say the result is &a
will print

	the result is 5


It also allows to solve aliases, preceded by `@`.
For example, if a variable `b` has an alias `a` and a value of `6`:

	say @a = &@a
will print

	b = 6

## Useful commands

- `cls` clears the console screen.
- `exit` closes chalk.
- `help` displays the main help page; you can add the name of a command afterwards to print its specific help page.