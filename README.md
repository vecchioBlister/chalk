# chalk
Chalk is a very powerful calculator, it allows from basic arithmetic to powerful algebra.
Its key features are:
- quick Pythonic calculations
- easy-to-understand commands
- handy and powerful variable management
- numpy algebra (coming soon)

## Getting started

### The chalk repository

The easiest way to get your hands on some chalk, since it's still in development, is to clone this repository in its current state. There may be bugs and WIP features, but you'll definitely be on the bleeding edge.

chalk requires Python 3.x and `numpy` installed in order to work.

The main executable file is chalk.py; it contains all of the required functions and the CLI. It does **not** contain neither documentation, nor helpfiles, so it's recommended that you bring along all of the attached folders.

Within [./docs/](https://github.com/LionSpeck/chalk/tree/main/docs) you'll find all of the documentation, and [./docs/help/](https://github.com/LionSpeck/chalk/tree/main/docs/help) is where chalk keeps all of its helpfiles. It's not advised to edit any of these files.

The [./scripts/](https://github.com/LionSpeck/chalk/tree/main/scripts) folder contains some useful functions and script templates; feel free to check them out and edit them.
The ./variables/ folder contains variable files, and is the default path for chalk's save-and-exit feature (try `help exit` for more information).

---
### Documentation files ([./docs/](https://github.com/LionSpeck/chalk/tree/main/docs))

- [Interface](https://github.com/LionSpeck/chalk/blob/main/docs/Interface.md#chalk-documentation-the-command-line-interface)
- [Commands](https://github.com/LionSpeck/chalk/blob/main/docs/Commands.md#chalk-documentation-commands)

---
### Basic operation

In order to quickly evaluate expressions, you can type them preceded by `=`, or by the `calc` command. The result will be stored in the currently manipulated variable (`ans` by default), that you can see on the left of your command line. If you want an operation result, without it being stored, you can type your calculation preceded by `?`.

#### Variables

One of the most useful tools of a calculator is its ability to store variables; with chalk it's very easy to assign, delete and show your variables:
- `let` is the most useful command, as it allows you to create a new variable, without the risk of replacing an existing value. By typing `let a be 7`, you will assign 7 to the new variable `a`. If you currently have a value stored in your manipulated variable, and want to save it in another variable, you can simply type `let b` to create a new variable `b` that will have that value. Or, if you can't think of a variable name, you can just type `let`, and chalk will provide one for you.
- `set` is the brother of `let`, and will have the exact same functionality, except for checking whether that variable already exists: `set` will overwrite an existing variable in case the name provided already exists.

#### Lazy assignment

One of the coolest features of chalk is its ability to lazy-assign values to variables: what this means, is that the variable value will be calculated every time that variable is called, instead of when it is assigned. You can use this functionality with `let` and `set` commands, by preceding with `&` the value you want to store. For example, let's say you have two variables, `a` and `b`: by typing `let c be &a*b`, you will be creating a new variable, `c`, the value of which (`a*b`) will be resolved every time `c` is called, and will depend on the values of `a` and `b`.

#### Print variables

Whenever you want to print the list of currently assigned variables and their values, you can use the command `var`: without any argument, it will print the full list of variables; you can put as many variable names as you wish, to filter the output to the given ones only. The results are ordered, by default, chronologically; in both cases, you can add the optional argument `-a` to order the results alphabetically.

#### Manipulation

Variable manipulation is a key feature of chalk, and it allows you to have a variable always-at-hand, to store all of your results. Whenever you type a calculation (with the `calc` command or its alias `=`), the result is stored in the manipulated variable (`ans` by default). If you want to change the currently-manipulated variable, you can use the `man` command, followed by a variable of your choice. If you want to go back to `ans`, you can just type `man` without any arguments, to select `ans`.

#### Deletion

When you want to delete a variable, you can use the `del` command, followed by how many variable names you wish to delete.
To delete all variables, simply type `del *`.

If the currently manipulated variable is deleted, `man` will automatically revert the manipulation to `ans`.
Note that you can't delete the `ans` variable, and remember that all variable deletions are permanent.

---
### Other useful commands

- `save` writes the assigned variables in a csv file.
- `load` imports saved variables from a chalk csv variables file.
- `run` runs a script file, executing each line as a command.


- `cls` clears the console screen.
- `exit` closes chalk.
- `help` displays the main help page; you can add the name of a command afterwards to print its specific help page.