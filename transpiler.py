import click
from click import Option, UsageError
import re
import os
from rich import print
import time

indentLevel = 0

tokens = (
    "MEMORY_SET",
    "INPUT",
    "OUTPUT",
    "RAW",
    "ASCII",
    "ADD",
    "SUB",
    "NUMBER",
    "START_LOOP",
    "END_LOOP",
    "GOTO",
    "IF",
    "END_IF",
    "RIGHT",
    "LEFT",
)

tokenRegexes = {
    "MEMORY_SET": r"memory",
    "INPUT": r"input",
    "OUTPUT": r"output",
    "RAW": r"raw",
    "ASCII": r"ascii",
    "ADD": r"add",
    "SUB": r"sub",
    "NUMBER": r"\d+",
    "GOTO": r"goto",
}

nodes = (
    "SET_MEMORY",
    "INPUT_ASCII",
    "INPUT_RAW",
    "OUTPUT_ASCII",
    "OUTPUT_RAW",
    "ADD",
    "SUB",
)

nodeRegexes = {
    "SET_MEMORY": r"^memory (\d+)$",
    "INPUT_ASCII": r"^input ascii$",
    "INPUT_RAW": r"^input raw$",
    "OUTPUT_ASCII": r"^output ascii$",
    "OUTPUT_RAW": r"^output raw$",
    "ADD": r"^add (\d+)$",
    "SUB": r"^sub (\d+)$",
    "BEGIN_LOOP": r"^loop$",
    "END_LOOP": r"^end loop$",
    "GOTO": r"^goto (\d+)$",
    "START_IF": r"^if (\d+)$",
    "END_IF": r"^end if$",
    "RIGHT": r"^right$",
    "LEFT": r"^left$"
}

def transpileDictionary():
    global indentLevel
    def memory(number):
        return f'memory = [0 for _ in range({number})]'
    
    def input_raw(*args, **kwargs):
        return 'memory[pointer] = int(input())'
    
    def input_ascii(*args, **kwargs):
        return 'memory[pointer] = ord(input())'
    
    def output_raw(*args, **kwargs):
        return 'print(memory[pointer], end="")'

    def output_ascii(*args, **kwargs):
        return 'print(chr(memory[pointer]), end="")'
    
    def add(number, *args, **kwargs):
        return f'memory[pointer] += {number}'
    
    def sub(number, *args, **kwargs):
        return f'memory[pointer] -= {number}'
    
    def begin_loop(*args, **kwargs):
        global indentLevel
        indentLevel += 1
        return 'while memory[pointer] != 0:'

    def end_loop(*args, **kwargs):
        global indentLevel
        indentLevel -= 1
        return ''

    def goto(number, *args, **kwargs):
        return f'pointer = {number}'

    def start_if(number, *args, **kwargs):
        global indentLevel
        indentLevel += 1
        return f'if memory[pointer] == {number}:'

    def end_if(*args, **kwargs):
        global indentLevel
        indentLevel -= 1
        return ''

    def right(*args, **kwargs):
        return 'pointer += 1'

    def left(*args, **kwargs):
        return 'pointer -= 1'

    return {
        "SET_MEMORY": memory,
        "INPUT_ASCII": input_ascii,
        "INPUT_RAW": input_raw,
        "OUTPUT_ASCII": output_ascii,
        "OUTPUT_RAW": output_raw,
        "ADD": add,
        "SUB": sub,
        "BEGIN_LOOP": begin_loop,
        "END_LOOP": end_loop,
        "GOTO": goto,
        "START_IF": start_if,
        "END_IF": end_if,
        "RIGHT": right,
        "LEFT": left,
    }

def transpile(file: str, outputFile: str):
    with open(file, "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    
    # Remove empty lines
    lines = [line for line in lines if line]

    # Run through all nodeRegexes and append a tuple of (nodeName, matches_in_regex)
    nodes = []
    for line in lines:
        for node in nodeRegexes:
            matches = re.findall(nodeRegexes[node], line)
            if matches:
                nodes.append((node, matches))

    # If there is no file named [outputFile], create it
    if not os.path.isfile(outputFile):
        with open(outputFile, "w") as f:
            f.write("")
    
    with open(outputFile, "w") as f:
        f.write("pointer = 0\n")
        for node in nodes:
            f.write(f"{'    ' * indentLevel}{transpileDictionary()[node[0]](*node[1])}\n")

class MutuallyExclusiveOption(Option):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop('mutually_exclusive', []))
        help = kwargs.get('help', '')
        if self.mutually_exclusive:
            ex_str = ', '.join(self.mutually_exclusive)
            kwargs['help'] = help + (
                ' NOTE: This argument is mutually exclusive with '
                ' arguments: [' + ex_str + '].'
            )
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(
                    self.name,
                    ', '.join(self.mutually_exclusive)
                )
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(
            ctx,
            opts,
            args
        )

# Create a click command
# The command takes in a required argument for the input file and an optional path for the output file, which is "output.py" by default
# The --silent flag can be used
# The --ctexe flag can be used to create an executable
@click.command()
@click.argument("inputFile", type=click.Path(exists=True))
@click.option("--outputFile", "-o", default="output.py", type=click.Path())
@click.option("--silent", "-s", is_flag=True)
@click.option("--ctexe", "-c", is_flag=True)
@click.option("--run", '-r', is_flag=True, help="Run the output file after transpiling", cls=MutuallyExclusiveOption, mutually_exclusive=['rexe'])
@click.option("--runexe", '-re', is_flag=True, help="Run the output file after transpiling", cls=MutuallyExclusiveOption, mutually_exclusive=['run'])
def main(inputfile, outputfile, silent, ctexe, run, runexe):
    if not silent:
        print(f"[blue]ChocoScript V2 Transpiler[/blue]")
        time.sleep(1.4)
        print(f"[yellow]Transpiling [/yellow][blue]{inputfile}[/blue][yellow] to [/yellow][blue]{outputfile}[/blue][yellow]...[/yellow]")
        time.sleep(1.4)
    transpile(inputfile, outputfile)
    if not silent:
        time.sleep(1.4)
        print(f"[green]Transpilation complete![/green]")
    if ctexe:
        if not silent:
            time.sleep(1.4)
            print(f"[yellow]Creating executable [/yellow][blue]{outputfile}[/blue][yellow]...[/yellow]")
        os.system(f"pyinstaller {outputfile} -y")
        if not silent:
            time.sleep(1.4)
            print(f"[light green]Executable created![/light green]")
    
    if run:
        if not silent:
            time.sleep(1.4)
            print(f"[yellow]Running [/yellow][blue]{outputfile}[/blue][yellow]...[/yellow]")
        os.system(f"{outputfile}")
        if not silent:
            time.sleep(1.4)
            print(f"[light green]Done![/light green]")
    elif runexe:
        if not silent:
            time.sleep(1.4)
            print(f"[yellow]Running [/yellow][blue]{outputfile}[/blue][yellow]...[/yellow]")
        os.system(f"build\\output\\{outputfile[:-3]}")
        if not silent:
            time.sleep(1.4)
            print(f"[light green]Done![/light green]")

if __name__ == "__main__":
    main()