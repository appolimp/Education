from math import sqrt

num = [2, 4, 9, 16, 25]


def s1(data):
    new_data = []
    for n in data:
        new_data.append(sqrt(n))
    return new_data


s2 = lambda data: list(map(sqrt, data))
s3 = lambda data: [sqrt(i) for i in data]


def s4(data):
    for n in data:
        yield sqrt(n)


print(s1(num))
print(s2(num))
print(s3(num))
print(list(s4(num)))
