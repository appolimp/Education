def knapsack_without_reps_BU(W, values_and_weights):
    n = len(values_and_weights)
    D = [[0] * (W + 1) for _ in range(n+1)]
    c, w = list(map(list, zip(*values_and_weights)))
    for i in range(1, n+1):
        for b in range(W + 1):
            D[i][b] = D[i-1][b]
            if w[i-1] <= b:
                D[i][b] = max(D[i][b], D[i-1][b -w[i-1]] + c[i-1])
    return D[-1][-1], D


def knapsack_with_reps_BU(W, values_and_weights):
    D = [0] * (W + 1)
    for b in range(W + 1):
        for c, w in values_and_weights:
            if w <= b:
                D[b] = max(D[b], D[b - w] + c)
    return D[W], D


def knapsack_TD(W, values_and_weights):
    n = len(values_and_weights)
    c, w = list(map(list, zip(*values_and_weights)))
    H = {}

    def knapsack(b):
        if b not in H:
            v = 0
            for i in range(n):
                if w[i] <= b:
                    v = max(v, knapsack(b - w[i]) + c[i])
            H[b] = v
        return H[b]

    knapsack(W)
    return H


def main():
    with open('1.txt') as f:
        reader = (list(map(int, line.split())) for line in f)
        capacity, n = next(reader)
        values_and_weights = list(reader)[0]
    assert len(values_and_weights) == n
    print(values_and_weights)
    # print(knapsack_with_reps_BU(capacity, values_and_weights))
    print()
    # num, res = knapsack_without_reps_BU(capacity, values_and_weights)
    # print(num, end= ' ')
    # [print(row) for row in res]

    recur = knapsack_TD(capacity, values_and_weights)
    print(recur)


if __name__ == '__main__':
    main()