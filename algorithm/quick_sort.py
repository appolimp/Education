import bisect
from random import randint


def quick_sort_dec(mas):

    def partition(mas, l, r):
        n = randint(l, r - 1)
        mas[l], mas[n] = mas[n], mas[l]
        x = mas[l]
        j = l
        k = l
        for i in range(l + 1, r):
            if mas[i] < x:
                j += 1
                mas[i], mas[j] = mas[j], mas[i]
            elif mas[i] == x:
                k += 1
                j += 1
                mas[i], mas[j], mas[k] = mas[j], mas[k], mas[i]
        mas[l], mas[j] = mas[j], mas[l]
        return j

    def quick_sort(mas, l, r):
        while l < r:
            m = partition(mas, l, r)
            quick_sort(mas, l, m)
            l = m + 1

    quick_sort(mas, 0, len(mas))

    return mas


def find_a(left, right, arg):
    result = []
    for elem in arg:
        count_left = bisect.bisect_right(left, elem)
        count_right = bisect.bisect_left(right, elem)
        result.append(count_left-count_right)
    return result


def main():
    # with sys.stdin as f:
    with open('quick_sort.txt') as f:
        reader = (map(int, line.split()) for line in f)

        n, _ = list(next(reader))
        left = []
        right = []
        for _ in range(n):
            a, b = list(next(reader))
            left.append(a)
            right.append(b)
        arg = list(next(reader))

    print(n, list(zip(left, right)), *arg)
    # left.sort()
    # right.sort()
    print(*quick_sort_dec(left))
    print(*quick_sort_dec(right))

    result = find_a(left, right, arg)
    print(*result)


def test():
    from algorithm.timing import timed
    n = 5*10**4
    m = 5*10**4
    left = []
    right = []
    for _ in range(n):
        a = randint(0, 10 ** 2)
        b = randint(0, 10 ** 2)
        a, b = sorted([a, b])
        left.append(a)
        right.append(b)
    arg = [randint(0, 10 ** 8) for _ in range(m)]

    print(n, m)
    time_1a = timed(quick_sort_dec, left)
    time_1b = timed(quick_sort_dec, right)
    time_2 = timed(find_a, left, right, arg)

    result = find_a(left, right, arg)

    return ['sort ==', time_1a + time_1b, '\nfind ==', time_2, '\n==', time_1a + time_1b + time_2]


if __name__ == '__main__':
    main()
    print(*test())