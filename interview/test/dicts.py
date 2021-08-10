class Node(object):
    def __init__(self, value, left=None, right=None):
        self.left = left
        self.right = right
        self.value = value  # 1 символ от 'A' до 'Z'


from collections import defaultdict
set_nodes = defaultdict(list)


def calc_set(root):
    k = {root.value}
    size = 1

    if root.left:
        left_set, left_size = calc_set(root.left)

        k.update(left_set)
        size += left_size

    if root.right:
        right_set, right_size = calc_set(root.right)

        k.update(right_set)
        size += right_size

    set_nodes[frozenset(k)].append((size, root))
    return k, size


def find_eq(nodes):
    if len(nodes) < 2:
        return None, None

    a, b = sorted([nodes[0], nodes[1]])[::-1]

    for x in nodes[2:]:
        if x[0] > a[0]:
            b = a
            a = x

        else:
            if x[0] > b[0]:
                b = x

    return a, b


def solve(root: Node) -> Optional[tuple[Node, Node]]:
    calc_set(root)

    max_dist, max_nodes = 0, None

    for nodes in set_nodes.values():
        first, second = find_eq(nodes)
        if first:
            if first[0] + second[0] > max_dist:
                max_dist = first[0] + second[0]
                max_nodes = (first[1], second[1])

    return max_nodes
