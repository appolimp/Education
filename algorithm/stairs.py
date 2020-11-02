def stairs_BU(n, values):
    D = [0] * n
    for i in range(n):
        D[i] = max(D[i-1], D[i-2]) + values[i]
    return D[-1]


def stairs_BU2(n, values):
    a, b = 0, values[0]
    for i in range(1, n):
        a, b = b, max(a, b) + values[i]
    return b


def stairs_TD(n, values):
    H = {}

    def stairs(i):
        if i not in H:
            if i < 0:
                return 0
            H[i] = max(stairs(i-1), stairs(i-2)) + values[i]
        return H[i]

    stairs(n - 1)
    return H[n-1]


def main():
    with open('1.txt') as f:
        reader = (list(map(int, line.split())) for line in f)
        n = next(reader)[0]
        values = next(reader)
    assert len(values) == n
    print(n, values)
    print('recu\t', stairs_TD(n, values))
    print('iter1\t', stairs_BU(n, values))
    print('iter2\t', stairs_BU2(n, values))


if __name__ == '__main__':
    main()