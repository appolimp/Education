color_base = {}

with open('1.txt') as f:
    for line in f:
        number, r, g, b = line.strip().split()
        color_base[number] = tuple(map(int, [r, g, b]))
print(color_base)
