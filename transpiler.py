# ChocoScript V2 Transpiler
#! By DarkWolf

import re
tokens = (
    'MEMORY_SET_TOKEN', 'POINTER_MANIPULATION_TOKEN', 'IOCMD', 'IOARG', 'NUMBER', 'MEMORY_ADDRESS'
)

tokenRegexes = {
    'MEMORY_SET_TOKEN': r'memory',
    'POINTER_MANIPULATION_TOKEN': r'goto',
    'IOCMD': r'input|output',
    'IOARG': r'raw|ascii',
    'NUMBER': r'\d+',
    'MEMORY_ADDRESS': r'\$\d+'
}

nodes = (
    'MEMORY_SET_NODE', 'POINTER_MANIPULATION_NODE', 'IONODE'
)

nodeSyntaxes = {
    'MEMORY_SET_NODE': 'MEMORY_SET_TOKEN NUMBER',
    'POINTER_MANIPULATION_NODE': 'POINTER_MANIPULATION_TOKEN MEMORY_ADDRESS',
    'IONODE': 'IOCMD IOARG'
}

nodeRegexes = {
    'MEMORY_SET_NODE': r'(memory) (\d+)',
    'POINTER_MANIPULATION_NODE': r'(goto) (\$\d+)',
    'IONODE': r'(input|output) (raw|ascii)'
}

def parse(code):
    for node, regex in nodeRegexes.items():
        if re.match(regex, code):
            # Return the matches in a list
            return re.findall(regex, code)

def IONode_instruction(token):
    if token[0] == 'input':
        if token[1] == 'raw':
            return f"memory[pointer] = int(input())"
        elif token[1] == 'ascii':
            return f"memory[pointer] = ord(input())"
    elif token[0] == 'output':
        if token[1] == 'raw':
            return f"print(chr(memory[pointer]))"
        elif token[1] == 'ascii':
            return f"print(memory[pointer])"

instructions = {
    "memory": lambda size: f"memory = [0 for _ in range({size})]",
    "goto": lambda address: f"pointer = {address}",
    "IONODE": IONode_instruction
}

# Run through every line in main.choco, remove the line endings and parse them

tokens = []

with open('main.choco', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line:
            tokens.append(parse(line))

toWrite = []
for token in tokens:
    if token[0][0] in ['input', 'output']:
        toWrite.append(IONode_instruction(token[0]))
    elif token[0][0] == 'memory':
        toWrite.append(instructions['memory'](token[0][1]))
    elif token[0][0] == 'goto':
        toWrite.append(instructions['goto'](token[0][1]))

with open('output.py', 'w') as f:
    f.write("pointer = 0\n")
    for line in toWrite:
        f.write(line + '\n')

