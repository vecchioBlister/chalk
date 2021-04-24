# chalk documentation: Commands

## calc

This command solves arithmetic expressions.
You can also call it more quickly with '='.
	
	calc 5+4

	=5+4
will store '9' in the currently manipulated variable.

You can also get results without storing the value, by calling 'calc' with '?':

	?5+4
will print the result '9' without assigning it.

You can also use variables and math (python module) constants in your calculations.

###### Note: within expressions, you must separate variable names with whitespaces, to avoid ambiguity: for instance, '1+ a + b \*8+6'.

## Variables

These two commands allow you to store variables.

### let

Allows you to create a new variable, without replacing an existing value.

	let <var> be <value>
stores a new variable \<var> with the value \<value>. If it exists already, you will get an error.

	let <var>
stores a new variable \<var> with the currently manipulated value.

	let
stores a new variable, with a random one-letter name that isn't being used, with the currently manipulated value.


### set

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

### var

Prints the list of currently stored variables.

You can give as arguments the names of the variables you want to display, separated by whitespaces.

By default, they're ordered chronologically; you can order them alphabetically by adding '-a'.
