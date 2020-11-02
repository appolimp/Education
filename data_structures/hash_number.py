class NumberBook:
    def __init__(self):
        self.data = ['not found'] * 10**7

    def add(self, num, name):
        self.data[num] = name

    def find(self, num):
        return self.data[num]

    def delete(self, num):
        self.data[num] = 'not found'


if __name__ == '__main__':
    with open('1.txt') as f:
        n = int(f.readline())
        book = NumberBook()

        for _ in range(n):
            com, number, *name = f.readline().split()
            number = int(number)
            if com == 'add':
                book.add(number, name[0])
            elif com == 'find':
                print(book.find(number))
            elif com == 'del':
                book.delete(number)


