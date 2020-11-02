class DisjointSet:
    def __init__(self, data):
        self.data = [0] + data
        self.parent = [0] + [i+1 for i in range(len(data))]
        self.max_len = max(self.data)

    def get_root(self, i):
        if i != self.parent[i]:
            self.parent[i] = self.get_root(self.parent[i])
        return self.parent[i]

    def union(self, destination, source):
        destination = self.get_root(destination)
        source = self.get_root(source)

        if source != destination:
            self.data[destination] += self.data[source]
            self.data[source] = 0
            self.parent[source] = destination

            self.max_len = max(self.max_len, self.data[destination])

    def get_max(self):
        return self.max_len


if __name__ == '__main__':
    with open('1.txt') as f:
        reader = (list(map(int, line.split())) for line in f)
        n, m = next(reader)
        data = next(reader)

        dis = DisjointSet(data)

        for dest, sour in reader:
            dis.union(dest, sour)
            print(dis.get_max())



