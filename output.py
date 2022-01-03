pointer = 0
memory = [0 for _ in range(256)]
memory[pointer] = int(input())
if memory[pointer] == 1:
    pointer = 1
    memory[pointer] = int(input())
    pointer = 2
    memory[pointer] = int(input())
    while memory[pointer] != 0:
        memory[pointer] -= 1
        pointer = 1
        memory[pointer] += 1
        pointer = 2
        
    pointer = 1
    print(memory[pointer])
    
if memory[pointer] == 2:
    pointer = 1
    memory[pointer] = int(input())
    pointer = 2
    memory[pointer] = int(input())
    while memory[pointer] != 0:
        memory[pointer] -= 1
        pointer = 1
        memory[pointer] -= 1
        pointer = 2
        
    pointer = 1
    print(memory[pointer])
    
