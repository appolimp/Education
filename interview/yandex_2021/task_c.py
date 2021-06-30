"""
Task C. Расстояние
"""

from collections import Counter


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
def find_dist(a_i, counter, k):
    items = [0] * counter[a_i]
    values = list(counter)
    index = values.index(a_i)

    for i in range(1, len(counter)):
        if len(items) > k:
            break

        count_a_plus = counter[values[index - i]] if index - 1 >= 0 else 0
        count_a_minus = counter[values[index + i]] if index + 1 <= len(counter) else 0

        items.extend(count_a_plus * [i]) if count_a_plus else None
        items.extend(count_a_minus * [i]) if count_a_minus else None

    print(items)
    return sum(items[:k+1])


def main():
    k, a = read_input('input.txt')
    counter = Counter(sorted(a))

    f = (find_dist(a_i, counter, k) for a_i in a)
    write_answer('output.txt', f)


if __name__ == '__main__':
    main()
