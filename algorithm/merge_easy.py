def merge_req(left, right, count=0):
    i = j = 0
    out = []
    while len(out) < len(left) + len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
            count += len(left) - i
        if i == len(left) or j == len(right):
            out.extend(left[i:] or right[j:])

    return out, count


def count_req(A):
    count = []

    def merge_sort_req(A):
        if len(A) < 2:
            return A
        middle = len(A) // 2
        new, count_new = merge_req(merge_sort_req(A[:middle]), merge_sort_req(A[middle:]))
        count.append(count_new)
        return new

    merge_sort_req(A)
    return sum(count)


def main_req():
    # import sys
    # with sys.stdin as f:
    with open('1.txt') as f:
        n = int(f.readline().strip())
        A = [int(i) for i in f.readline().strip().split()]
    print(n, A)

    print(count_req(A))


if __name__ == '__main__':
    main_req()
