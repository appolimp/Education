import sys
sys.setrecursionlimit(20000)

res = True


def check(data, key, min_=float('-inf'), max_=float('inf')):
    global res
    if key == -1 or not res:
        return
    value, left, right = data[key]
    if min_ <= value < max_:
        check(data, left, min_, value)
        check(data, right, value, max_)
    else:
        res = False


def is_correct(data):
    if data:
        check(data, 0)

    return 'CORRECT' if res else 'INCORRECT'


def main():
    # with sys.stdin as f:
    with open('1.txt') as f:
        reader = (tuple(map(int, line.split())) for line in f)
        n = next(reader)[0]
        data = [val for val in reader]

    print(is_correct(data))


if __name__ == '__main__':
    main()
