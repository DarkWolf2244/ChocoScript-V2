pointer = 0
memory = [0 for _ in range(256)]
memory[pointer] += 62
pointer = 1
memory[pointer] += 32
pointer = 2
memory[pointer] += 13
pointer = 3
memory[pointer] += 10
pointer = 5
memory[pointer] += 1
while memory[pointer] != 0:
    pointer = 0
    print(chr(memory[pointer]), end="")
    pointer = 1
    print(chr(memory[pointer]), end="")
    pointer = 6
    memory[pointer] = ord(input())
    if memory[pointer] == 97:
        pointer = 7
        memory[pointer] = int(input())
        pointer = 8
        memory[pointer] = int(input())
        while memory[pointer] != 0:
            memory[pointer] -= 1
            pointer = 7
            memory[pointer] += 1
            pointer = 8
            
        pointer = 7
        print(memory[pointer], end="")
        
    if memory[pointer] == 115:
        pointer = 7
        memory[pointer] = int(input())
        pointer = 8
        memory[pointer] = int(input())
        while memory[pointer] != 0:
            memory[pointer] -= 1
            pointer = 7
            memory[pointer] -= 1
            pointer = 8
            
        pointer = 7
        print(memory[pointer], end="")
        
    if memory[pointer] == 101:
        pointer = 5
        memory[pointer] -= 1
        
    pointer = 3
    print(chr(memory[pointer]), end="")
    pointer = 5
    
