import sys


def insert(value):
    global code
    code += [int(value)]
    i = len(code) - 1
    b = 0
    if len(code) % 2 == 1:
        code[i//2], code[i] = sorted([code[i], code[i//2]], reverse=True)
        i = i // 2
    while code[i] > code[i // 2] and i > 1:
        code[i // 2], code[i//2*2], code[i//2*2+1] = sorted([code[i // 2], code[i//2*2], code[i//2*2+1]], reverse=True)
        i = i // 2


def extract():
    global code
    # print(code)
    value, new_value = code.pop(1), code.pop()
    code.insert(1, new_value)
    i = 1
    while (2*i+1) < len(code):
        b = 0 if code[2*i] >= code[2*i+1] else 1
        if code[i] >= code[2*i+b]:
            code[i], code[2*i+b] = code[2*i+b], code[i]
            i = 2 * i + b
        else:
            break
    if 2*i < len(code):
        code[i], code[2*i] = max(code[i], code[2*i]), min(code[i], code[2*i])
    return value


code = [0]
# with sys.stdin as f:
with open('1.txt') as f:
    n = int(f.readline().strip())
    for _ in range(n):
        com, *val = f.readline().strip().split()
        print(com, val)
        if com == 'Insert':
            insert(val[0])
            print(code)
        else:
            print(extract())
            print(code)
