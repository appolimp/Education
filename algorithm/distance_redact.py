def diff(a, b):
    return 0 if a == b else 1


def edit_dist_td(first, second):
    n = len(first) + 1
    m = len(second) + 1
    D = [[float('inf')] * m for _ in range(n)]
    i, j = n-1, m-1

    def edit_dist(i, j):
        if D[i][j] == float('inf'):
            if i == 0 or j == 0:
                D[i][j] = j or i
            else:
                ins = edit_dist(i, j - 1) + 1
                del0 = edit_dist(i - 1, j) + 1
                sub = edit_dist(i - 1, j - 1) + diff(first[i-1], second[j-1])
                D[i][j] = min(ins, del0, sub)
        return D[i][j]

    edit_dist(i, j)
    return D


def edit_dist_bu(first, second):
    n = len(first) + 1
    m = len(second) + 1

    D = [[0] * m for _ in range(n)]

    for i in range(n):
        D[i][0] = i
    for j in range(m):
        D[0][j] = j

    for i in range(1, n):
        for j in range(1, m):
            c = diff(first[i-1], second[j-1])
            D[i][j] = min(D[i-1][j] + 1, D[i][j-1] + 1, D[i-1][j-1] + c)
    return D


def main():
    # import sys
    # with sys.stdin as f:
    with open('1.txt') as f:
        first = f.readline().strip()
        second = f.readline().strip()
    print(first, '~~~', second)
    td = edit_dist_td(first, second)
    bu = edit_dist_bu(first, second)
    [print(row) for row in td]
    print()
    [print(row) for row in bu]



if __name__ == '__main__':
    main()
