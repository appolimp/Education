# line = input()
line = 'abacabad'
freq = [[i, line.count(i)] for i in set(line)]
print(len(freq), end=' ')
code = {}
if len(freq) == 1:
    code[freq[0][0]] = ['','', '0']
while len(freq) > 1:
    freq.sort(key=lambda x: x[1], reverse=True)
    m1, m2 = freq.pop(), freq.pop()
    new = [m1[0] + m2[0], m1[1] + m2[1]]
    code[new[0]] = [m1[0], m2[0], '']
    code.setdefault(m1[0], ['', '', '0'])
    code[m1[0]][-1] = '0'
    code.setdefault(m2[0], ['', '', '1'])
    code[m2[0]][-1] = '1'
    freq.append(new)
    # print(code)

def name(parent):
    child1, child2, cod = code[parent]
    if child1:
        code[child1][-1] = cod + code[child1][-1]
        name(child1)
    if child2:
        code[child2][-1] = cod + code[child2][-1]
        name(child2)



name(freq[0][0])
out = ''
for s in line:
    # print(s, code[s])
    out += code[s][-1]
print(len(out))
[print(key+': '+val[-1]) for key, val in sorted(code.items()) if len(key) == 1]


print(out)
