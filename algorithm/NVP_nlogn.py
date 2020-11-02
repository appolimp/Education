def find_nvp(mas):
    D = [float('-inf')] * (len(mas) + 5)
    pos = [-1] * (len(D))
    prev = [0] * len(mas)
    D[0] = float('inf')

    for i, elem in enumerate(mas):
        left = 0
        right = len(D) - 1
        while left < right:
            middle = (left + right) // 2
            if elem <= D[middle]:
                left = middle + 1
            else:
                right = middle
        if D[right] < elem:
            D[right] = elem
            pos[right] = i
            prev[i] = pos[right - 1]
    j = D.index(float('-inf')) - 1
    print(j)
    result = []
    i = pos[j]
    while i != -1:
        result.append(i + 1)
        i = prev[i]

    return result[::-1]


def main():
    # import sys
    # with sys.stdin as f:
    with open('1.txt') as f:
        n = int(f.readline().strip())
        mas = [int(i) for i in f.readline().strip().split()]
        print(n, mas)

    print(*find_nvp(mas))


if __name__ == '__main__':
    main()
