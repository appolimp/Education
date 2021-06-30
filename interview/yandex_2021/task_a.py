

def read_input(path):
    with open(path) as f:
        n = int(next(f))
        volumes = [int(i) for i in next(f).split()]

    return n, volumes


def is_possible(volumes):
    return False


def calculate_count(volumes):
    pass


def main():
    n, volumes = read_input('input.txt')
    count_operation = calculate_count(volumes) if is_possible(volumes) else -1
    print(count_operation)


if __name__ == '__main__':
    main()
