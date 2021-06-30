"""
Task F. Спутниковая съёмка
"""

from collections import Counter


def write_answer(path, data):
    with open(path, 'w') as f:
        f.write('\n'.join(str(i) for i in data))


def main():

    left_corners_and_days = {}

    with open('input.txt') as f:
        n = int(next(f))
        snapshots = ([int(i) for i in row.split()] for row in f)

        for day, (x1, y1, x2, y2) in enumerate(snapshots):
            if x1 == x2 or y1 == y2:
                continue

            left_corners = ((x1+dx, y1+dy) for dx in range(x2 - x1) for dy in range(y2 - y1))
            left_corners_and_days.update(dict.fromkeys(left_corners, day))

    days = Counter(left_corners_and_days.values())
    block_count = (days.get(i, 0) for i in range(n))

    write_answer('output.txt', block_count)


if __name__ == '__main__':
    main()
