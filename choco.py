import click
from click import Option, UsageError
import transpiler
import time
import os
from rich import print

@click.group()
def cli():
    pass

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

# Transpile command:
# Transpile a file to a new file
# Options:
#     -i, --input: Input file (required)
#     -o, --output: Output file (default: output.py)
#     -s, --silent: Don't print anything
#     -c, --ctexe: Create an executable
@cli.command()
@click.argument("inputFile", type=click.Path(exists=True))
@click.option("--outputFile", "-o", default="output.py", type=click.Path(), help="The output file to transpile to")
@click.option("--silent", "-s", is_flag=True, help="Say absolutely nothing (way faster)")
@click.option("--ctexe", "-c", is_flag=True, help="Create an executable from the output file, stored in the /build directory")
@click.option("--run", '-r', is_flag=True, help="Run the output file after transpiling", cls=MutuallyExclusiveOption, mutually_exclusive=['rexe'])
@click.option("--runexe", '-re', is_flag=True, help="Run the output file after transpiling", cls=MutuallyExclusiveOption, mutually_exclusive=['run'])
def transpile(inputfile, outputfile, silent, ctexe, run, runexe):
    """Transpile a .choco file to Python. Optionally create an executable of the output file with PyInstaller."""
    if not silent:
        print(f"[blue]ChocoScript V2 Transpiler[/blue]")
        time.sleep(1.4)
        print(f"[yellow]Transpiling [/yellow][blue]{inputfile}[/blue][yellow] to [/yellow][blue]{outputfile}[/blue][yellow]...[/yellow]")
        time.sleep(1.4)
    transpiler.transpile(inputfile, outputfile)
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

if __name__ == '__main__':
    cli()
