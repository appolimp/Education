import bisect


def find_nkp(mas):
    D = [0]*len(mas)
    for i in range(len(mas)):
        D[i] = 1
        for j in range(i):
            if mas[i] % mas[j] == 0 and D[j] + 1 > D[i]:
                D[i] = D[j] + 1
    return max(D)


def main():
    # import sys
    # with sys.stdin as f:
    with open('1.txt') as f:
        n = int(f.readline().strip())
        mas = [int(i) for i in f.readline().strip().split()]
        print(n, mas)

    print(find_nkp(mas))


if __name__ == '__main__':
    main()