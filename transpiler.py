import click
import re
import os

tokens = (
    "MEMORY_SET",
    "INPUT",
    "OUTPUT",
    "RAW",
    "ASCII",
    "ADD",
    "SUB",
    "NUMBER"
)

tokenRegexes = {
    "MEMORY_SET": r"memory",
    "INPUT": r"input",
    "OUTPUT": r"output",
    "RAW": r"raw",
    "ASCII": r"ascii",
    "ADD": r"add",
    "SUB": r"sub",
    "NUMBER": r"\d+"
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
    "SUB": r"^sub (\d+)$"
}

def transpileDictionary():
    def memory(number):
        return f'memory = [0 for _ in range({number})]'
    
    def input_raw(*args, **kwargs):
        return 'memory[pointer] = int(input())'
    
    def input_ascii(*args, **kwargs):
        return 'memory[pointer] = ord(input())'
    
    def output_raw(*args, **kwargs):
        return 'print(memory[pointer])'

    def output_ascii(*args, **kwargs):
        return 'print(chr(memory[pointer]))'
    
    def add(number, *args, **kwargs):
        return f'memory[pointer] += {number}'
    
    def sub(number, *args, **kwargs):
        return f'memory[pointer] -= {number}'
    
    return {
        "SET_MEMORY": memory,
        "INPUT_ASCII": input_ascii,
        "INPUT_RAW": input_raw,
        "OUTPUT_ASCII": output_ascii,
        "OUTPUT_RAW": output_raw,
        "ADD": add,
        "SUB": sub
    }

def transpile(file: str, outputFile: str):
    with open(file, "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    
    # Remove empty lines
    lines = [line for line in lines if line]

    # Run through all nodeRegexes and append a tuple of (nodeName, matches_in_regex)
    nodes = []
    for node in nodeRegexes:
        for line in lines:
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
            f.write(f"{transpileDictionary()[node[0]](*node[1])}\n")

if __name__ == "__main__":
    print(transpile("main.choco", "output.py"))