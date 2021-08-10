from collections import defaultdict


def read_input():
    with open('input.txt') as f:
        n = int(next(f))
        towns_ = [tuple(map(int, next(f).split())) for _ in range(n)]
        k_ = int(next(f))
        start_, end_ = map(int, next(f).split())

    return towns_, k_, start_, end_


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


towns, k, start, end = read_input()

graph = defaultdict(list)
for i, a in enumerate(towns):
    for j, b in enumerate(towns[i+1:], start=i+1):
        if dist(a, b) <= k:
            graph[i+1].append(j+1)
            graph[j+1].append(i+1)

visited = {start}
deque = [start]
level = 0

while deque:
    node = deque.pop(0)
    level += 1

    if end in graph[node]:
        print(level)
        break

    for neighbor in graph[node]:
        if neighbor not in visited:
            visited.add(neighbor)
            deque.append(neighbor)

else:
    print(-1)
