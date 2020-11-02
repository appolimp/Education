import heapq


def fractional_knapsack(capacity, values_and_weights):
    order = [(-v / w, w) for v, w in values_and_weights]
    heapq.heapify(order)

    acc = 0
    while order and capacity:
        v_per_w, w = heapq.heappop(order)
        can_take = min(w, capacity)
        acc -= v_per_w * can_take
        capacity -= can_take

    return acc


def fractional_knapsack2(capacity, values_and_weights):
    order = [(-v / w, w) for v, w in values_and_weights]
    order.sort()

    acc = 0
    for v_per_w, w in order:
        can_take = min(w, capacity)
        acc -= v_per_w * can_take
        capacity -= can_take
        if capacity == 0:
            break

    return acc


def main():
    with open('1.txt') as f:
        reader = (tuple(map(int, line.split())) for line in f)
        n, capacity = next(reader)
        values_and_weights = list(reader)
    assert len(values_and_weights) == n
    opt_value = fractional_knapsack(capacity, values_and_weights)
    print('{:.3f}'.format(opt_value))


def test1(num):
    from random import randint
    from algorithm.timing import timed
    to1 = []
    to2 = []
    for attempt in range(num):
        n = randint(1, 1000)
        capacity = randint(0, 2 * 10**6)
        values_and_weights = []
        for _ in range(n):
            values_and_weights.append((randint(0, 2 * 10*6), randint(1, 2 * 10**6)))
        t1 = timed(fractional_knapsack, capacity, values_and_weights)
        t2 = timed(fractional_knapsack2, capacity, values_and_weights)
        to1.append(t1)
        to2.append(t2)
    return [to1, to2]


def graf(t1, t2):
    from matplotlib import pyplot as plt
    # fig, axs = plt.subplots(1, 2, sharey='all', sharex=True, tight_layout=True)
    fig, axs = plt.subplots()
    axs.hist(t1, facecolor='red', alpha=1, label='heap')
    axs.hist(t2, facecolor='green', alpha=0.25, label='sort')
    axs.legend(loc=1)
    plt.show()


if __name__ == '__main__':
    t1, t2 = test1(500)
    graf(t1, t2)

