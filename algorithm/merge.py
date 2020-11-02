def merge(A, B, C, l, r, count=0):
    m = l + (r - l) // 2
    l_b = l
    r_b = l_c = m
    r_c = r
    out = []
    while l_b < r_b and l_c < r_c:
        if B[l_b] <= C[l_c]:
            out.append(B[l_b])
            l_b += 1
        else:
            out.append(C[l_c])
            count += r_b - l - l_b
            l_c += 1

    if l_b == r_b or l_c == r_c:
        out.extend(B[l_b:r_b] or C[l_c:r_c])

    A[l:r_c] = out

    return A, count


def merge_count(A, l, r):
    count = []

    def merge_sort(A, l, r):
        if r - l > 1:
            m = l + (r - l) // 2
            A, new_count = merge(A, merge_sort(A, l, m), merge_sort(A, m, r), l, r)
            count.append(new_count)
            return A
        return A

    merge_sort(A, l, r)
    return count, sum(count)


def merge_req(left, right, count=0):
    i = j = 0
    out = []
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            out.append(left[i])
            # print(i, left, left[i], '~~~', j, right, right[j], '~~~', len(left))
            i += 1

        else:
            out.append(right[j])
            j += 1
            count += len(left) - i

    if i < len(left) or j < len(right):
        out.extend(left[i:] or right[j:])
    return out, count


def count_req(A):
    count = []

    def merge_sort_req(A):
        if len(A) > 1:
            middle = len(A) // 2
            new, count_new = merge_req(merge_sort_req(A[:middle]), merge_sort_req(A[middle:]))
            count.append(count_new)
            return new
        else:
            return A

    merge_sort_req(A)
    return sum(count)


def nativ_count(n, A):
    count = 0
    for i in range(n):
        for j in range(i+1, n):
            if A[i] > A[j]:
                count += 1
    return count



def main():
    # import sys
    # with sys.stdin as f:
    with open('1.txt') as f:
        n = int(f.readline().strip())
        A = [int(i) for i in f.readline().strip().split()]
    print(n, A)
    # print(merge_count(A, 0, n))
    print(nativ_count(n, A))
    # print(count_req(A))


def test():
    from random import randint
    from algorithm.timing import timed
    n = 10 ** 4
    A = []
    for _ in range(n):
        A.append(randint(0, 10 ** 9))
    time_1 = timed(merge_count, A, 0, n)
    time_2 = timed(sorted, A)
    time_3 = timed(count_req, A)
    time_4 = timed(nativ_count, n, A)
    return ['merge ==', time_1, '\nsort ==', time_2, '\nmerge < sort ==', time_1 < time_2, '\nreq ==', time_3, '\nnativ ==', time_4]


if __name__ == '__main__':
    main()
    print(*test())
