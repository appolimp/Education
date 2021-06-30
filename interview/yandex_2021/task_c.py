"""
Task C. Расстояние
"""


def read_input(path):
    with open(path) as f:
        n, k = [int(i) for i in next(f).split()]
        a = [int(i) for i in next(f).split()]

    return k, a


def write_answer(path, data):
    with open(path, 'w') as f:
        f.write(' '.join(str(i) for i in data))


def find_dist(a_i, a, k):
    print(a)

    index = a.index(a_i)
    start = (index - k) if index - k > 0 else 0

    items = a[start: index + k]
    print(a_i, index, items)

    a_modules = sorted(abs(a_j - a_i) for a_j in a)

    return sum(a_modules[1:k+1])  # +1, так как пропускаем а_i


def main():
    k, a = read_input('input.txt')
    a.sort()

    f = [find_dist(a_i, a[:], k) for a_i in a]
    write_answer('output.txt', f)


if __name__ == '__main__':
    main()
