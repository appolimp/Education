class DisjointSet:
    def __init__(self, data):
        self.parent = [0] + [i + 1 for i in range(len(data))]

    def get_root(self, i):
        if i != self.parent[i]:
            self.parent[i] = self.get_root(self.parent[i])
        return self.parent[i]

    def union(self, destination, source):
        destination = self.get_root(destination)
        source = self.get_root(source)

        if source != destination:
            self.parent[source] = destination

    def intersect(self, i, j):
        return self.get_root(i) == self.get_root(j)


if __name__ == '__main__':
    with open('1.txt') as f:
        reader = (list(map(int, line.split())) for line in f)
        n, e, d = next(reader)
        data = list(range(n))

        dis = DisjointSet(data)

        for _ in range(e):
            i, j = next(reader)
            dis.union(i, j)

        for _ in range(d):
            i, j = next(reader)
            if dis.intersect(j, i):
                print(0)
                break
        else:
            print(1)
