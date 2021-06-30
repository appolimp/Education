"""
Task A. Андрей и кислота
"""


def read_input(path):
    with open(path) as f:
        n = int(next(f))
        volumes = [int(i) for i in next(f).split()]

    return n, volumes


def is_possible(volumes):
    return all(first <= second for first, second in zip(volumes, volumes[1:]))


def calculate_count(volumes):
    return volumes[-1] - volumes[0]


def write_answer(path, data):
    with open(path, 'w') as f:
        f.write(str(data))


def main():
    _, volumes = read_input('input.txt')
    count_operation = calculate_count(volumes) if is_possible(volumes) else -1
    write_answer('output.txt', count_operation)


if __name__ == '__main__':
    main()
