def gcd(a, b):
    return gcd(b, a % b) if b else a


def fib_mod(n, m):

    modul = [0, 1]
    prev, cur = [0, 1]
    for i in range(2, n + 1):
        prev, cur = cur, (prev + cur) % m
        modul.append(cur % m)
        if modul[-2:] == [0, 1]:
            k = n % (len(modul) - 2)
            print(modul[k])
            break
    else:
        print(cur % m)


def main():
    # import sys
    # with sys.stdin as f:
    with open('1.txt') as f:
        reader = (map(int, line.split()) for line in f)
        n, m = list(next(reader))
    print(n, m)
    print(fib_mod(n, m))


if __name__ == '__main__':
    main()