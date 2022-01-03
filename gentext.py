def gen(text):
    i = 0
    for c in text:
        print(f"add {ord(c)}")
        i += 1
        print(f"goto {i}")

gen("That's a zero.")