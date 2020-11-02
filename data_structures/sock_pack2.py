class Buffer:
    def __init__(self, size, n):
        self._size = size
        self.log = [0] * n
        self._buffer = []

    def add_pack(self, i, arr, dur):

        if self._check(arr):
            self._push(i, arr, dur)
        else:
            self.log[i] = -1

    def _push(self, i, arr, dur):
        if not self._buffer:
            start = arr
        else:
            start = self._buffer[-1][-1]

        self._buffer.append((i, start, start + dur))

    def _check(self, time):
        # print(self.log, self._buffer)
        if not self._buffer:
            return True

        while self._buffer:
            if self._buffer[0][-1] <= time:
                i, start, end = self._buffer.pop(0)
                self.log[i] = start
            else:
                break

        if len(self._buffer) >= self._size:
            return False
        else:
            return True

    def get_log(self):
        for i, start, end in self._buffer:
            self.log[i] = start

        return self.log


if __name__ == '__main__':
    with open('1.txt') as f:
        reader = (tuple(map(int, line.split())) for line in f)
        size, n = next(reader)
        buffer = Buffer(size, n)
        for i, (arr, dur) in enumerate(reader):
            buffer.add_pack(i, arr, dur)

    print(*buffer.get_log(), sep='\n')