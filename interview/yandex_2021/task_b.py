"""
Task B. Посадка в самолет
"""


def read_input(path):
    with open(path) as f:
        n = int(next(f))
        seats = [next(f).strip() for _ in range(n)]

        m = int(next(f))
        passengers = [next(f).strip() for _ in range(m)]

    return seats, passengers


def write_answer(path, data):
    with open(path, 'w') as f:
        f.write(str(data))


class Plane:
    def __init__(self, seats):
        self.left_seats = self.convert_by_side(seats, side=0)
        self.right_seats = self.convert_by_side(seats, side=1)

    def get_passenger(self, count, is_right, is_window):
        side_seats = self.right_seats if is_right else self.left_seats

        for i_row, row in enumerate(side_seats):
            first_place = self._calculate_first_place(count, is_window)
            if all(row[first_place:first_place + count]):
                mask = [first_place == 0, count > 1, first_place > 0 or count == 3]
                side_seats[i_row] = [False if new else old for old, new in zip(row, mask)]

                places = self._find_place(i_row, mask, is_right)

                print(f'Passengers can take seats: {places}')
                print(self._busy_place(i_row, mask, is_right))

                return

        print('Cannot fulfill passengers requirements')

    @staticmethod
    def _find_place(i_row, mask, is_right):
        letters_by_side = 'FED' if is_right else 'ABC'

        letters = [let for place, let in zip(mask, letters_by_side) if place]
        letters = letters[::-1] if is_right else letters

        places = ' '.join(f'{i_row+1}{let}' for let in letters)
        return places

    @staticmethod
    def _calculate_first_place(count, is_window):
        if count == 3 or is_window:
            return 0
        if count == 2:
            return 1
        return 2

    def convert_to_answer(self):
        left_side = [['.' if place else '#' for place in row] for row in self.left_seats]
        right_side = [['.' if place else '#' for place in row[::-1]] for row in self.right_seats]
        rows = [''.join(left) + '_' + ''.join(right) for left, right in zip(left_side, right_side)]

        return '\n'.join(rows)

    def _busy_place(self, i_row, mask, is_right):
        left_side = [['.' if place else '#' for place in row] for row in self.left_seats]
        right_side = [['.' if place else '#' for place in row[::-1]] for row in self.right_seats]

        side = right_side if is_right else left_side
        mask = mask[::-1] if is_right else mask

        side[i_row] = ['X' if new else old for old, new in zip(side[i_row], mask)]

        rows = [''.join(left) + '_' + ''.join(right) for left, right in zip(left_side, right_side)]
        return '\n'.join(rows)




    @staticmethod
    def convert_by_side(seats, side=0):
        step = -1 if side else 1  # right
        return [[place == '.' for place in row.split('_')[side]][::step] for row in seats]


def main():
    seats, passengers = read_input('input.txt')
    plane = Plane(seats)

    for passenger in passengers:
        count_str, side, position = passenger.split()
        plane.get_passenger(count=int(count_str), is_right=side == 'right', is_window=position == 'window')


if __name__ == '__main__':
    main()
