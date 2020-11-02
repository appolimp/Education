class Avl:
    root = None

    # FIXME
    def __new__(cls, *args, **kwargs):
        """Нужно что то сделать при удалении последнего корня"""
        if Avl.root is None:
            Avl.root = super().__new__(cls)
            return Avl.root
        return super().__new__(cls)

    def __init__(self, value=None, parent=None):
        self.left = None
        self.right = None
        self.parent = parent
        self.height = 1
        if self is Avl.root and value:
            self.append(value)
            value = None
        self.key = value

    def append(self, other):
        side = 'left' if (self is Avl.root) or (other < self.key) else 'right'
        if getattr(self, side) is None:
            setattr(self, side, Avl(other, self))
            self.reload_height()
        else:
            getattr(self, side).append(other)

    def reload_height(self):
        if self is Avl.root:
            return
        left = self.left.height if self.left else 0
        right = self.right.height if self.right else 0
        self.height = max(left, right) + 1
        self.rotation()
        if self.parent:
            self.parent.update()

    def rotation(self):
        def is_height_wrong():
            if self.left is None and self.right is None:
                return False
            l = self.left.height if self.left else 0
            r = self.right.height if self.right else 0
            return abs(l - r) > 1

        # Правое малое вращение
        if self.right and not(self.parent is None) and is_height_wrong():
            right = self.right

            self.parent.new_child(self, right)
            self.parent, self.right, right.left = right, right.left, self

            if self.right:
                self.right.parent = self
            self.reload_height()

        # Левое малое вращение
        if self.left and not(self.parent is None) and is_height_wrong():
            # print(self, repr(self), is_height_wrong())
            left = self.left

            self.parent.new_child(self, left)
            self.parent, self.left, left.right = left, left.right, self

            if self.left:
                self.left.parent = self
            self.reload_height()

    def find(self, value):
        if self is Avl.root:
            return self.left
        if value == self.key:
            return self
        if (value > self.key and self.right is None) or (value < self.key and self.left is None):
            return None

        return (self.left if value < self.key else self.right).find(value)

    def find_min(self):
        if self.left is None:
            return self
        return self.left.find_min()

    def find_max(self):
        if self.right is None:
            return self
        return self.right.find_max()

    def next_val(self, value):
        item = self.find(value)
        if item is None:
            return None
        if item.right:
            return item.right.find_min()

        while item.parent:
            if item.parent.left == item:
                return item.parent
            item = item.parent

        return None

    def prev_val(self, value):
        item = self.find(value)
        if item is None:
            return None
        if item.left:
            return item.left.find_max()

        while item.parent:
            if item.parent.right == item:
                return item.parent
            item = item.parent

        return None

    def new_child(self, old, new):
        if not (new is None):
            new.parent = self
        if old == self.left:
            self.left = new
        else:
            self.right = new

    def _del(self):
        def prepare(side):
            self.parent.new_child(old=self, new=side)
            self.reload_height()

        # Лист FIXME обработать удаление единственного корня
        if (self.left is None) and (self.right is None):
            if self.parent is None:
                Avl.root = None
            return prepare(None)

        # Корень только слева
        if self.right is None:
            return prepare(self.left)

        # Корень только справа
        if self.left is None:
            return prepare(self.right)

        # Узел с двумя корнями
        next_ = self.next_val(self.key)
        next_.key, self.key = self.key, next_.key
        next_._del()

    def del_val(self, value):
        item = self.find(value)
        if item is None:
            raise KeyError
        return item._del()

    def __str__(self):
        return ' '.join(str(x) for x in (self.left, self.key, self.right) if x)

    def __repr__(self):
        return '\t'.join([str(x.key if x else '-') for x in
                          (self, self.left, self.right, self.parent)] + [str(self.height)])

    def printer(self):
        self.left.printer() if self.left else None
        print(repr(self))
        self.right.printer() if self.right else None


class MyAvlTree:
    def __init__(self):
        self.heap = []

    def append(self, value) -> None:

        if not self.heap:
            self.heap.append([value, -1, -1, -1, 0])
            return

        self.find_place(value)

    def find_val(self, value, i=0):
        key, left, right, *_ = self.heap[i]
        if value == key:
            return i
        if (value > key and right == -1) or (value < key and left == -1):
            return 'Not found'

        return self.find_val(value, left if value < key else right)

    @staticmethod
    def parent(i):
        return (i - 1) // 2

    def find_min(self, i=0):
        key, left, *_ = self.heap[i]
        j = i
        while left != -1:
            j = left
            key, left, *_ = self.heap[left]
        return j

    def find_max(self, i=0):
        key, _, right, *_ = self.heap[i]
        j = i
        while right != -1:
            j = right
            key, _, right, *_ = self.heap[right]
        return j

    def next_val(self, value):
        i = self.find_val(value)
        if i == 'Not found':
            return 'Not found current value'

        key, left, right, par, _ = self.heap[i]
        if right != -1:
            return self.find_min(right)

        j = par
        while par != -1:
            key, left, right, par, _ = self.heap[par]
            if left == i:
                return j
            i, j = j, par

        return 'Next val not exist'

    def prev_val(self, value):
        i = self.find_val(value)
        if i == 'Not found':
            return 'Not found current value'

        key, left, right, par, _ = self.heap[i]
        if left != -1:
            return self.find_max(left)

        j = par
        while par != -1:
            key, left, right, par, _ = self.heap[par]
            if right == i:
                return j
            i, j = j, par

        return 'Prev val not exist'

    def reload_height(self, i):
        _, left, right, par, _ = self.heap[i]
        if left == right == -1:
            height = 0
        else:
            height = max(self.heap[left][4], self.heap[right][4]) + 1

        self.heap[i][4] = height
        if par == -1:
            return
        self.reload_height(par)

    def insert(self, j, value):
        while len(self.heap) <= j:
            t_par = self.parent(len(self.heap))
            self.heap.append([None, -1, -1, t_par, 0])

        par = self.parent(j)
        self.heap[j] = [value, -1, -1, par, 0]
        self.reload_height(par)

    def find_place(self, value, i=0):

        key, left, right, par, height = self.heap[i]
        if key is None:
            j = i
            par = self.parent(i)
            self.heap[par][i - 2 * par] = i
            self.insert(j, value)

        elif value >= key:
            if right == -1:
                right = 2 * i + 2
                self.heap[i][2] = right
                self.insert(right, value)
            else:
                self.find_place(value, right)

        else:
            if left == -1:
                left = 2 * i + 1
                self.heap[i][1] = left
                self.insert(left, value)
            else:
                self.find_place(value, left)

    def del_val(self, value):
        i = self.find_val(value)
        if i == 'Not found':
            return 'Not found current value'
        self.del_val_i(i)

    def del_val_i(self, i):
        def rel_par(i, left_right):  # left == 1, right == 2
            par = self.parent(i)
            self.heap[i] = [None, -1, -1, par, 0]
            self.heap[par][left_right] = -1
            self.reload_height(par)

        key, left, right, par, _ = self.heap[i]
        if left == right == -1:
            left_right = self.heap[par].index(i)
            rel_par(i, left_right)

        elif left == -1:
            self.heap[right][3] = self.heap[i][3]
            self.heap[i], self.heap[right] = self.heap[right], self.heap[i]
            rel_par(right, 2)

        elif right == -1:
            self.heap[left][3] = self.heap[i][3]
            self.heap[i], self.heap[left] = self.heap[left], self.heap[i]
            rel_par(left, 1)

        else:
            next = self.next_val(self.heap[i][0])
            self.heap[i][0], self.heap[next][0] = self.heap[next][0], self.heap[i][0]
            self.del_val_i(next)

    def get_heap(self, i):
        key, left, right, *_ = self.heap[i]
        left_heap = self.get_heap(left) if left != -1 else []
        main_heap = [key] if not (key is None) else []
        right_heap = self.get_heap(right) if right != -1 else []
        return left_heap + main_heap + right_heap

    def __str__(self):
        return ' '.join(str(i) for i in self.get_heap(0))


if __name__ == '__main__':
    cool = Avl(2)
    cool.append(5)
    cool.append(7)
    cool.append(5)
    cool.append(4)
    cool.append(3)

    """
    cool.append(5)
    cool.append(7)
    cool.append(1)
    cool.append(6)
    cool.append(8)
    cool.append(9)
   """

    print(cool)
    print('\t'.join('k l r p h'.split()))
    print('=' * 17)
    cool.printer()

    print('-' * 10)

    # cool.del_val(5)
    # cool.printer()

    """
    heap = MyAvlTree()
    heap.append(9)
    heap.append(11)
    heap.append(12)
    heap.append(10)
    heap.del_val(12)
    heap.del_val(10)

    heap.append(7)
    heap.append(12)
    heap.append(10)
    heap.append(5)
    heap.append(9)
    heap.append(15)
    heap.append(1)

    print(heap)
    print(*heap.heap)
    # print(heap.next_val(11))
    """