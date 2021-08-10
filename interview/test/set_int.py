def read_input():
    with open('input.txt') as f:
        t, d, n = map(int, next(f).split())  # noqa
        points_ = [map(int, line.split()) for line in f]

    return t, d, n, points_


class Position:
    def __init__(self, x, y, time):
        self.time = time

        self.max_lr = x - y + time
        self.min_lr = x - y - time

        self.max_td = x + y + time
        self.min_td = x + y - time

    def update(self, x, y, err):
        new_pos = self.__class__(x, y, err)

        self.max_lr = min(self.max_lr, new_pos.max_lr) + self.time
        self.min_lr = max(self.min_lr, new_pos.min_lr) - self.time

        self.max_td = min(self.max_td, new_pos.max_td) + self.time
        self.min_td = max(self.min_td, new_pos.min_td) - self.time

    def final_points(self):
        maybe = []
        for x_minus_y in range(self.min_lr + self.time, self.max_lr - self.time + 1):
            for x_plus_y in range(self.min_td + self.time, self.max_td - self.time + 1):
                if (x_minus_y + x_plus_y) % 2 == 0:
                    x = (x_minus_y + x_plus_y) // 2
                    y = x - x_minus_y
                    maybe.append(f'{x} {y}')

        return maybe


t, d, n, points = read_input()
pos = Position(x=0, y=0, time=t)

for x_i, y_i in points:
    pos.update(x_i, y_i, d)

final_points = pos.final_points()
print(len(final_points), *final_points, sep='\n')


