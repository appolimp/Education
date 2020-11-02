import sys


def binary_search(num, mass, cache):
    if num in cache:
        return cache[num]

    left = 0
    right = len(mass)

    while left < right:
        middle = (left + right) // 2

        if mass[middle] == num:
            cache[num] = middle
            return middle

        if mass[middle] > num:
            right = middle
        else:
            left = middle + 1
    return -1


def main():
    cache = {}
    with open('1.txt') as f:
        mass = [int(i) for i in f.readline().strip().split()]
        _, *search = [int(i) for i in f.readline().strip().split()]
    return [binary_search(num, mass, cache) for num in search]


if __name__ == '__main__':

    print(*main())
