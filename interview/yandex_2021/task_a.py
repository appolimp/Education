"""
Task A. Андрей и кислота
"""

import random


def read_input(path):
    with open(path) as f:
        n = int(next(f))
        volumes = [int(i) for i in next(f).split()]

    return n, volumes


def is_possible(volumes):
    return all(first <= second for first, second in zip(volumes, volumes[1:]))


def calculate_count(volumes):
    count_iteration = sum(max(volumes) - volume for volume in set(volumes))
    return count_iteration


def write_answer(path, data):
    with open(path, 'w') as f:
        f.write(str(data))

    print(data)


def main():
    _, volumes = read_input('input.txt')
    # volumes = [random.randint(1, 100) for _ in range(10)]
    volumes.sort()
    print(volumes)
    count_operation = calculate_count(volumes) if is_possible(volumes) else -1
    write_answer('output.txt', count_operation)


if __name__ == '__main__':
    main()
