class MinHeap:
    def __init__(self, data):
        self.data = data
        self.size = len(data) - 1
        self.log = []

    def move_down(self, i):
        left = 2*i + 1
        right = 2 * i + 2

        if left > self.size:
            return

        if left == self.size:
            j = left

        elif right <= self.size:
            j = [left, right][self.data[left] > self.data[right]]

        if self.data[j] < self.data[i]:
            self.log.append((i, j))
            self.data[i], self.data[j] = self.data[j], self.data[i]
            self.move_down(j)

    def reload(self):
        for i in range(self.size, -1, -1):
            self.move_down(i)

    def print_log(self):
        print(len(self.log))
        for row in self.log:
            print(*row)


if __name__ == '__main__':
    with open('1.txt') as f:
        n = int(f.readline())
        data = [int(i) for i in f.readline().split()]
        # data = list(range(100, 0, -1))

    heap = MinHeap(data)
    heap.reload()
    heap.print_log()

