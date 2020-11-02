import sys


def shift_up(i):
    while heap[i] > heap[(i - 1) // 2] and i != 0:
        heap[i], heap[(i - 1) // 2] = heap[(i - 1) // 2], heap[i]
        i = (i - 1) // 2


def shift_down(i):
    while 2 * i + 1 < len(heap):
        left = 2 * i + 1
        right = 2 * i + 2
        j = left
        if right < len(heap) and heap[right] > heap[left]:
            j = right
        if heap[i] > heap[j]:
            break
        heap[i], heap[j] = heap[j], heap[i]
        i = j


heap = []
# with sys.stdin as f:
with open('1.txt') as f:
    n = int(f.readline().strip())
    for _ in range(n):
        req, *num = f.readline().strip().split()
        # print(req, num)
        if req == 'Insert':
            num = int(num[0])
            heap.append(num)
            shift_up(len(heap) - 1)
        else:
            print(heap[0])
            heap[0] = heap.pop()
            shift_down(0)
            # print(heap)
