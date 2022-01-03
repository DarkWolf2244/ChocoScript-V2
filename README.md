# ChocoScript V2

ChocoScript is a sort-of esoteric language created by me while trying to figure out how languages parsed and lexed. It's incredibly simple, and similar to Brainf*ck.

## How it works
Like Brainf*ck, ChocoScript is based on an array resembling a Turing Tape. It can store only numbers. There's a pointer that can slide along the "tape" and you can interact with the number it's on.

### Moving along the memory array
Moving along this "tape" is easy - use **"goto [int]"** to **jump to a specific index** on the array. The array is **zero-indexed**, which means it starts from 0.

You also have "right" and "left" which can be used to move right and left on the array if you need it.

### Changing values on the memory array
There's **`ADD [int]` and `SUB [int]`** to **add** and **subtract** to the **current location** in memory.

### Input/Output
This one's a bit more complex. You use two basic commands - **`input [raw/ascii]`** and **`output [raw/ascii]`**. 

Use `raw` if you want to **display the actual number in memory or save the number literally**. An error will be thrown if the user enters anything that `int()` can't parse.

Use `ascii` to **find the corresponding ASCII character** and display that to screen (like for text) or **save the characted entered as its ASCII value**. An error will be thrown if the user enters anything `ord()` or `chr()` can't parse.

### Loops
Yeah, there are loops. Here's an example of one.

```
  memory 256
  
  input raw
  
  loop
    output raw
    sub 1
   end loop
```

The loop will only **enter if the current value isn't 0** (< or >) and will only **break when the current value _is_ 0**. The above program takes a number from the user and prints all the numbers below until 0. **Indenting isn't necessary.** Also, **remember to end it with `end loop`**.

### Conditional logic
Conditional logic is narrowed down to **IF statements**.

```
  memory 256
  
  input raw
  

  if 1
    goto 2
    input raw
    add 5
    output raw
  end if
    
  if 2
     goto 2
     input raw
     sub 5
     output raw
  end if
 ```
 
 `If` **takes a number and executes the code inside if the current value is that number**. Remember to **end it with `end if`**.
 
 ### Defining Memory
 You can set the size of the memory array with `memory [int]` at the start.
 
 ## Executing
 ChocoScript transpiles to Python. Yes, it's slow, but we're not going for speed here. You can optionally use PyInstaller to package the transpiled file into an executable.
 
 Write your code in a file preferably ending in `.choco`. Use the Choco CLI (`choco.py`) to transpile the code.

The help page:
```
Usage: choco.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  transpile  Transpile a .choco file to Python.

```

The help page for the `transpile` command:
```
Usage: choco.py transpile [OPTIONS] INPUTFILE

  Transpile a .choco file to Python. Optionally create an executable of the
  output file with PyInstaller.

Options:
  -o, --outputFile PATH  The output file to transpile to
  -s, --silent           Say absolutely nothing (way faster)
  -c, --ctexe            Create an executable from the output file, stored in
                         the /build directory

  -r, --run              Run the output file after transpiling NOTE: This
                         argument is mutually exclusive with  arguments:
                         [rexe].

  -re, --runexe          Run the output file after transpiling NOTE: This
                         argument is mutually exclusive with  arguments:
                         [run].

  --help                 Show this message and exit.
```

Have fun with it.
