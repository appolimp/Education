"""
Task F. Спутниковая съёмка
"""


def read_input(path):
    with open(path) as f:
        _ = next(f)
        snapshots = [[int(i) for i in row.split()] for row in f]

    return snapshots


def write_answer(path, data):
    with open(path, 'w') as f:
        f.write('\n'.join(str(i) for i in data))


def get_left_corners_from_snapshots(snapshot):
    x1, y1, x2, y2 = snapshot

    if x1 == x2 or y1 == y2:
        return set()

    left_corners = set()
    for dx in range(x2 - x1):
        for dy in range(y2 - y1):
            left_corners.add((x1+dx, y1+dy))

    return left_corners


def main():
    snapshots = read_input('input.txt')

    actual_photo = set()
    count_photo_per_days = []

    for snapshot in snapshots[::-1]:
        photo = get_left_corners_from_snapshots(snapshot)
        actual_photo.update(photo)
        count_photo_per_days.append(len(actual_photo))

    count_new_photo_per_day = [count_photo_per_days[0]] + [now - last for now, last in zip(count_photo_per_days[1:],
                                                                                           count_photo_per_days)]
    write_answer('output.txt', count_new_photo_per_day[::-1])


if __name__ == '__main__':
    main()
