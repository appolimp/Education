def knapsack_without_reps_BU(W, w):
    n = len(w)
    D = [[0] * (W + 1) for _ in range(n+1)]
    for i in range(1, n+1):
        for b in range(W + 1):
            D[i][b] = D[i-1][b]
            if w[i-1] <= b:
                D[i][b] = max(D[i][b], D[i-1][b - w[i-1]] + w[i-1])
    return D[-1][-1]


def main():
    with open('1.txt') as f:
        reader = (list(map(int, line.split())) for line in f)
        capacity, n = next(reader)
        weights = list(reader)[0]
    assert len(weights) == n
    print(weights)
    recur = knapsack_without_reps_BU(capacity, weights)
    print(recur)


if __name__ == '__main__':
    main()