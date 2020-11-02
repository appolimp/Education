def count_sort(mas, n):
    B = [0 for _ in range(12)]
    A_new = [0 for _ in range(n+1)]
    for j in range(n):
        B[mas[j]] += 1
    print(B)
    for i in range(1, 11):
        B[i] += B[i-1]
    print(B)
    for j in range(n-1, -1, -1):
        A_new[B[mas[j]]] = mas[j]
        B[mas[j]] -= 1
    return A_new


def main():
    import sys
    # with sys.stdin as f:
    with open('1.txt') as f:
        n = int(f.readline().strip())
        mas = [int(i) for i in f.readline().strip().split()]
    print(n, mas)

    B = [0] * 11
    for i in mas:
        B[i] += 1
    for j in range(11):
        if B[j] : print(*[str(j)]*B[j], end=' ')



if __name__ == '__main__':
    main()