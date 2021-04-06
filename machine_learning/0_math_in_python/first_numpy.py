import numpy as np


def main():
    a = np.arange(3, 13).reshape((2, -1))
    print(repr(np.array(a)))

    print(repr((a > 5) & ~(a < 10)))

    b = a.astype(str)
    print(repr(np.array(b)))


if __name__ == '__main__':
    main()
