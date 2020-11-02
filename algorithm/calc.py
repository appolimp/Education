def calc_BU(n):
    D = [[float('inf')] * 4 for _ in range(n)]
    for j in range(n):
        D[j][0] = j + 1
    for i in range(1, 4):
        D[0][i] = 0
    for j in range(1, n):
        D[j][1] = min(D[j-1][1:]) + 1
        if (j+1) % 2 == 0:
            D[j][2] = min(D[j//2][1:]) + 1
        if (j+1) % 3 == 0:
            D[j][3] = min(D[j//3][1:]) + 1
    return D


def ret_calc_BU(n, D):
    arr = [n]
    j = len(D) - 1
    while n != 1:
        ind = D[j].index(min(D[j]))
        if ind == 3:
            n = n // 3
            j = j // 3
            arr.append(n)
        elif ind == 2:
            n = n // 2
            j = j // 2
            arr.append(n)
        else:
            n -= 1
            j -= 1
            arr.append(n)

    return arr[::-1]


def calc_TD(n):
    H = {1: 0}

    def calc(i):
        if i not in H:
            dubl = 1 + calc(i // 2) if i % 2 == 0 else float('inf')
            tripl = 1 + calc(i // 3) if i % 3 == 0 else float('inf')
            dif = 1 + calc(i - 1) if i > 1 else float('inf')
            H[i] = min(dubl, tripl, dif)
        return H[i]

    return calc(n)


def main():
    with open('1.txt') as f:
        reader = (list(map(int, line.split())) for line in f)
        n = next(reader)[0]
    print(n)
    print('recu\t', calc_TD(n))
    res = calc_BU(n)
    number = min(res[-1])
    print('iter\t', number)
    [print(row) for row in res]
    arr = ret_calc_BU(n, res)
    print([len(arr)], *arr)


if __name__ == '__main__':
    main()
