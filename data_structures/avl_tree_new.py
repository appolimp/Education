from abc import ABC, abstractmethod
from copy import copy, deepcopy
import random
import sys


class AvlMeta(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def append(self, value):
        pass

    @abstractmethod
    def find(self, value):
        pass

    @abstractmethod
    def min(self):
        pass

    @abstractmethod
    def max(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def printer(self):
        pass

    @staticmethod
    def next_val(value):
        pass

    @staticmethod
    def prev_val(value):
        pass


class Avl(AvlMeta):
    def __init__(self, values=None):
        self.key = 'r'
        self.child = None

        values is not None and self.extend(values)

    def update(self):
        pass

    def rotation(self):
        pass

    def append(self, value):
        if self.child is None:
            self.child = Knot(value, parent=self)
        else:
            self.child.append(value)

    def extend(self, value):
        temp = []
        if isinstance(value, set):
            value = list(value)
        if isinstance(value, list) or isinstance(value, tuple) and len(value) > 1:
            value, temp = value[0], value[1:]

        self.append(value)

        for val in temp:
            self.append(val)

    def find(self, value):
        if self.child is None:
            raise KeyError('Key not found')
        return self.child.find(value)

    def min(self):
        if self.child is None:
            raise ValueError('min() arg is an empty sequence')
        return self.child.min()

    def max(self):
        if self.child is None:
            raise ValueError('max() arg is an empty sequence')
        return self.child.max()

    def next_val(self, value):
        key = self.find(value)
        return self.child.next_key(key)

    def prev_val(self, value):
        key = self.find(value)
        return self.child.prev_key(key)

    def delete_val(self, value):
        key = self.find(value)
        key.delete()

    def del_child(self, child):
        if self.child is child:
            self.child = None

        child.par = None

    def new_child(self, old=None, new=None):
        self.child = new
        new.par = self

    def get_i(self, i):
        if self.child is None:
            raise IndexError('list index out of range')

        if i < 0:
            i = self.child.size + i

        if i > len(self) or i < 0:
            raise IndexError('list index out of range')

        return self.child.get_i(i + 1)  # +1 Для сохранения свойства питоноского листа

    @staticmethod
    def merge_root(left, right, key):
        if isinstance(left, Avl):
            left = left.child

        if isinstance(right, Avl):
            right = right.child

        new = Avl(key)
        new.child.left, new.child.right = left, right
        if left:
            left.par = new.child
        if right:
            right.par = new.child
        new.child.update()

        return new

    def merge(self, other):
        one = deepcopy(self)
        other = deepcopy(other)

        key = one.max()
        val = key.key
        key.delete()

        if abs(one.child.height - other.child.height) <= 1:
            return self.merge_root(one.child, other.child, val)
        elif one.child.height > other.child.height:
            one.child.merge_avl(other.child, val)
            return one
        else:
            other.child.merge_avl(one.child, val)
            return other

    def split(self, val):
        if self.child is None:
            raise KeyError('Key not found')
        return self.child.split(val)

    def get_sum(self, start, end):
        if end > start:
            return 0
        me = deepcopy(self)
        _, res = me.split(start-1)
        # res.printer()
        if res is None:
            return 0

        res, _ = res.split(end)
        if res is None:
            return 0
        return res.child.sum

    def get_sum_left(self, val):
        if self.child is None:
            raise NotImplemented
        return self.child.get_sum_left(val)

    def get_sum_right(self, val):
        if self.child is None:
            raise NotImplemented
        return self.child.get_sum_right(val)

    def get_summ(self, start, end):
        if self.child is None:
            return 0
        res = self.child.sum
        res -= self.get_sum_left(start)
        res -= self.get_sum_right(end)
        return res

    def __getitem__(self, item):
        return self.get_i(item)

    def __str__(self):
        if self.child is None:
            return ''
        return str(self.child)

    def __repr__(self):
        if self.child is None:
            return '[]'
        return repr(self.child)

    def __contains__(self, item):
        try:
            self.find(item)
        except KeyError:
            return False
        return True

    def __len__(self):
        if self.child is None:
            return 0
        return self.child.size

    def printer(self):
        if self.child:
            print('k l r p h s s'.replace(' ', '\t'))
            self.child.printer()
            print('-' * 21)
        else:
            print('[]')


class Knot(AvlMeta):

    def __init__(self, value, parent):
        self.key = value
        self.par = parent
        self.left = None
        self.right = None
        self.height = 1
        self.size = 1
        self.sum = self.key

    def update_size(self):
        left = self.left.size if self.left else 0
        right = self.right.size if self.right else 0
        self.size = left + right + 1

    def update_sum(self):
        left = self.left.sum if self.left else 0
        right = self.right.sum if self.right else 0
        self.sum = left + right + self.key

    def update_height(self, recur=True):
        left = self.left.height if self.left else 0
        right = self.right.height if self.right else 0
        self.height = max(left, right) + 1

    def update(self, recur=True):
        self.update_height()
        self.rotation()
        self.update_size()
        self.update_sum()
        if recur:
            self.par.update()

    def rotation(self):
        if self.how_right_higher() > 1:
            if self.right.how_right_higher() > 0:
                # print('small right\t', self.how_right_higher(), self.right.how_right_higher())
                self.rotation_small_right()
            else:
                # print('big right\t', self.how_right_higher(), self.right.how_right_higher())
                self.rotation_big_right()

            if self.right:
                self.right.par = self
                self.right.update_size()

        elif self.how_right_higher() < -1:
            if self.left.how_right_higher() <= 0:
                # print('small left\t', self.how_right_higher(), self.left.how_right_higher())
                self.rotation_small_left()
            else:
                # print('big left\t', self.how_right_higher(), self.left.how_right_higher())
                self.rotation_big_left()

            if self.left:
                self.left.par = self
                self.left.update_size()

    def how_right_higher(self):
        left = self.left.height if self.left else 0
        right = self.right.height if self.right else 0
        return right - left

    def rotation_small_right(self):
        self.par.new_child(old=self, new=self.right)
        self.right.left, self.right, self.par = self, self.right.left, self.right
        self.update()

    def rotation_big_right(self):
        gamma = self.right.left

        self.par.new_child(old=self, new=gamma)
        self.right.new_child(old=gamma, new=gamma.right)

        self.par = self.right.par = gamma
        gamma.left, gamma.right, self.right = self, self.right, gamma.left

        if gamma.right:
            gamma.right.update(recur=False)
        self.update()

    def rotation_small_left(self):
        self.par.new_child(old=self, new=self.left)
        self.left.right, self.left, self.par = self, self.left.right, self.left
        self.update()

    def rotation_big_left(self):
        gamma = self.left.right

        self.par.new_child(old=self, new=gamma)
        self.left.new_child(old=gamma, new=gamma.left)

        self.par = self.left.par = gamma
        gamma.right, gamma.left, self.left = self, self.left, gamma.right

        if gamma.left:
            gamma.left.update(recur=False)
        self.update()

    def new_child(self, old, new):
        side = 'left' if self.left and old is self.left else 'right'
        setattr(self, side, new)
        if new:
            new.par = self

    def append(self, value):
        side = 'left' if value < self.key else 'right'
        if getattr(self, side) is None:
            setattr(self, side, Knot(value, parent=self))
            self.update()
        else:
            getattr(self, side).append(value)

    def find(self, value):
        if value == self.key:
            return self

        side = getattr(self, 'left' if value < self.key else 'right')
        if side:
            return side.find(value)

        raise KeyError('Key not found')

    def min(self):
        if self.left is None:
            return self
        return self.left.min()

    def max(self):
        if self.right is None:
            return self
        return self.right.max()

    @staticmethod
    def next_key(key):
        if key.right:
            return key.right.min()

        while key.par.__class__ is not Avl:
            if key.par.left and key.par.left is key:
                return key.par
            key = key.par

        raise ValueError('don`t have next value')

    @staticmethod
    def prev_key(key):
        if key.left:
            return key.left.max()

        while key.par.__class__ is not Avl:
            if key.par.right and key.par.right is key:
                return key.par
            key = key.par

        raise ValueError('don`t have next value')

    def get_i(self, i):
        left_size = self.left.size if self.left else 0
        if i == left_size + 1:
            return self
        if i < left_size + 1:
            if self.left:
                return self.left.get_i(i)
            raise IndexError('list index out of range')
        elif self.right:
            return self.right.get_i(i - left_size - 1)

        raise IndexError('list index out of range')

    def delete(self):
        if (self.left is None) and (self.right is None):
            self.par.del_child(self)
        elif (self.left is None) or (self.right is None):
            side = getattr(self, 'left' if self.left else 'right')
            self.key = side.key
            side.delete()
        else:
            key = self.next_key(self)
            self.key = key.key
            key.delete()

    def del_child(self, child):
        if self.left is child:
            self.left = None
        elif self.right is child:
            self.right = None
        else:
            raise KeyError('child not found')  # Поидее сюда не должны доходить

        child.par = None
        self.update()

    def merge_avl(self, other, key: int):  # right
        if key > self.key:  # go right
            if abs(self.height - other.height) < 2:
                key = Knot(key, parent=self)
                key.right, other.par = other, key
                if self.right:
                    key.left, self.right.par = self.right, key
                self.right = key
                key.update()

            else:
                self.right.merge_avl(other, key)
        else:
            if abs(self.height - other.height) < 2:
                key = Knot(key, parent=self)
                key.left, other.par = other, key
                if self.left:
                    key.right, self.left.par = self.left, key
                self.left = key
                key.update()

            else:
                self.left.merge_avl(other, key)

        return key

    def split(self, val):
        if val < self.key:
            if self.left:
                left, right = self.left.split(val)
                right = Avl.merge_root(right, self.right, self.key)
                return left, right
            return None, Avl.merge_root(None, self.right, self.key)

        elif val > self.key:
            if self.right:
                left, right = self.right.split(val)
                left = Avl.merge_root(self.left, left, self.key)
                return left, right
            return Avl.merge_root(self.left, None, self.key), None

        elif val == self.key:
            left = Avl.merge_root(self.left, None, self.key)
            right = Avl.merge_root(None, self.right, self.key)
            right.delete_val(self.key)
            return left, right

    def get_sum_left(self, val):
        if self.key < val:
            left = self.left.sum if self.left else 0
            right = self.right.get_sum_left(val) if self.right else 0
            return left + self.key + right
        if self.key > val:
            return self.left.get_sum_left(val) if self.left else 0
        if self.key == val:
            return self.left.sum if self.left else 0

    def get_sum_right(self, val):
        if self.key > val:
            left = self.left.get_sum_right(val) if self.left else 0
            right = self.right.sum if self.right else 0
            return left + self.key + right
        if self.key < val:
            return self.right.get_sum_right(val) if self.right else 0
        if self.key == val:
            return self.right.sum if self.right else 0

    def __str__(self):
        return ' '.join(str(x) for x in (self.left, self.key, self.right) if not (x is None))

    def __repr__(self):
        return ('\t'.join((str(x.key) if x else '-') for x in (self, self.left, self.right, self.par))
                + '\t' + str(self.height)
                + '\t' + str(self.size)
                + '\t' + str(self.sum)
                )

    def __getitem__(self, item):
        return self.get_i(item)

    def printer(self):
        self.left and self.left.printer()
        print(repr(self))
        self.right and self.right.printer()


class Avl_control:
    def __init__(self):
        self.avl = Avl()
        self.last = 0

    def func(self, x):
        # return int(x)
        return (int(x) + self.last) % 1_000_000_001

    def __call__(self, line):
        com, *value = line.split()
        # print(com, value)
        if com == '?':
            return self._find(self.func(*value))
        if com == '+':
            self._add(self.func(*value))
        if com == '-':
            self._del(self.func(*value))
        if com == 's':
            l, r = [self.func(i) for i in value]
            self._sum(l, r)

    def _find(self, value):
        print('Found' if value in self.avl else 'Not found')

    def _add(self, value):
        if value not in self.avl:
            self.avl.append(value)

    def _del(self, value):
        if value in self.avl:
            self.avl.delete_val(value)

    def _sum(self, l, r):
        # print('~~~\t', self.avl.get_summ(l, r))
        self.last = self.avl.get_summ(l, r)
        print(self.last)

    def printer(self):
        self.avl.printer()


if __name__ == '__main__':

    a = Avl_control()
    # with sys.stdin as f:
    with open('1.txt') as f:
        n = f.readline()
        for line in f:
            if line == '\n':
                break
            a(line)

    a.printer()
    # print('~~'*10)
    """
    a.printer()
    left, right = a.avl.split(841558476)
    right.printer()
    left, right = right.split(217510399)
    """
    e = a.avl

    # print(e.get_sum_left(50))
    # print(e.get_sum_right(100))