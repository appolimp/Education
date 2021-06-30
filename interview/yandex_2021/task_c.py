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


def cache(func):
    result = {}

    def wraps(*args):
        a_i = args[0]
        if a_i not in result:
            result[a_i] = func(*args)

        return result[a_i]

    return wraps


@cache
def find_dist(a_i, a, k):
    index = a.index(a_i)
    k += 1  # так как пропускаем a_i

    start = (index - k) if index - k > 0 else 0
    items = a[start: index + k]

    distances = sorted(abs(a_j - a_i) for a_j in items)

    return sum(distances[:k])


def main():
    k, a = read_input('input.txt')
    a_sorted = sorted(a)

    f = [find_dist(a_i, a_sorted[:], k) for a_i in a]
    write_answer('output.txt', f)


if __name__ == '__main__':
    main()
