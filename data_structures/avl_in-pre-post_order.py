import sys


def in_order(data, key):
    if key == -1:
        return []
    value, left, right = data[key]
    return in_order(data, left) + [value] + in_order(data, right)


def pre_order(data, key):
    if key == -1:
        return []
    value, left, right = data[key]
    return [value] + pre_order(data, left) + pre_order(data, right)


def post_order(data, key):
    if key == -1:
        return []
    value, left, right = data[key]
    return post_order(data, left) + post_order(data, right) + [value]


def main():
    # with sys.stdin as f:
    with open('1.txt') as f:
        reader = (tuple(map(int, line.split())) for line in f)
        next(reader)
        data = [val for val in reader]
        print(data)

    print(*in_order(data, 0))
    print(*pre_order(data, 0))
    print(*post_order(data, 0))


if __name__ == '__main__':
    main()
