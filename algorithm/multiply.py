def bin_sum(x: list, y: list, *args: list) -> list:
    x = ''.join(x)
    y = ''.join(y)
    c = int(x, 2) + int(y, 2)
    for z in args:
        z = ''.join(z)
        c += int(z, 2)
    return list(f'{c:b}')


def bin_sum2(x: list, y: list, *args: list) -> list:
    out, w = [], 0
    n = max(len(x), len(y))
    for i in range(1, n+1):
        x0 = int(x[-i]) if i < len(x)+1 else 0
        y0 = int(y[-i]) if i < len(y)+1 else 0
        c0 = list(f'{y0+x0+w:b}')
        out.insert(0, c0.pop())
        w = 1 if c0 else 0
    out.insert(0, str(w))
    for z in args:
        out = bin_sum2(out, z)

    return out


def multiply(x, y):
    if not y:
        return ['0']
    y = y[:]
    even = y.pop()
    z = multiply(x, y)
    if even == '0':
        return z + ['0']
    else:
        return bin_sum2(x, z + ['0'])


def mul_int(a, b):
    d0 = a + b + b
    a = list(f'{a:b}')
    b = list(f'{b:b}')
    c = ''.join(multiply(a, b))
    return int(c, 2)


def mul_kar(a, b):
    a = list(f'{a:b}')
    b = list(f'{b:b}')
    c = ''.join(karatsuba(a, b))
    return int(c, 2)


def karatsuba(x: list, y: list) -> list:
    n = max(map(len, [x, y]))
    n += n % 2
    x, y = ['0'] * (n - len(x)) + x, ['0'] * (n - len(y)) + y
    if n <= 8:
        return multiply(x, y)

    k = n // 2
    x_l, x_r = x[:k], x[k:]
    y_l, y_r = y[:k], y[k:]

    p1 = karatsuba(x_l, y_l)
    p2 = karatsuba(x_r, y_r)
    p3 = karatsuba(bin_sum2(x_l, x_r), bin_sum2(y_l, y_r))

    return bin_sum(p1 + ['0'] * 2 * k, bin_sum(p3, ['-'] + p1, ['-'] + p2) + ['0'] * k, p2)


def main():
    a = 12
    b = 17
    c = mul_int(a, b)
    print(c)
    d = mul_kar(a, b)
    print(d)


def test(n=100):
    from random import randint
    from algorithm.timing import compare
    args = []
    for i in range(n):
        # args.append([i, i])
        args.append([randint(2 * 10 ** 40, 2 * 10 ** 50), randint(2 * 10 ** 40, 2 * 10 ** 50)])
    compare([mul_int, mul_kar], args)


if __name__ == '__main__':
    main()
    test(1000)
