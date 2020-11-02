from abc import ABC, abstractmethod
from copy import copy, deepcopy
import random
import sys
import time

sys.setrecursionlimit(10**9)
i = 0

class Avl:
    def __init__(self, values=None, child=None):
        self.key = 'r'
        self.child = child
        if child:
            child.par = self

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

    def min(self):
        if self.child is None:
            raise ValueError('min() arg is an empty sequence')
        return self.child.min()

    def max(self):
        if self.child is None:
            raise ValueError('max() arg is an empty sequence')
        return self.child.max()

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

        if isinstance(i, slice):
            out, res = self.get_slice(i.start, i.stop)
            return res

        if i < 0:
            i = self.child.size + i

        if i > len(self) or i < 0:
            raise IndexError('list index out of range')

        return self.child.get_i(i + 1)  # +1 Для сохранения свойства питоноского листа

    def get_slice(self, start, end):
        if self.child is None:
            raise IndexError('list index out of range')
        return self.child.get_slice(start, end)

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
        one = self
        other = other

        key = one.max()
        val = key.key
        key.delete()
        """
                if abs(one.child.height - other.child.height) <= 1:
                    return self.merge_root(one.child, other.child, val)
                elif one.child.height > other.child.height:
                    one.child.merge_avl(other.child, val)
                    return one
                else:
                    other.child.merge_avl(one.child, val)
                    return other
                """
        return self.merge_root(one.child, other.child, val)

    def split(self, val):
        if self.child is None:
            raise KeyError('Key not found')
        return self.child.split(val)

    def rope(self, i, j, k):
        if i == 0:
            left, right = self.split(j+1)
            out, res = right, left
        else:
            out, res = self.get_slice(i, j+1)

        # res.printer('res')
        # out.printer('out')

        if out.child is None:
            return res

        if k == 0:
            out.min().add_prev_brain(res.child)
        else:
            out[k-1].add_next_brain(res.child)

        return out

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

    def __len__(self):
        if self.child is None:
            return 0
        return self.child.size

    def printer(self, name=''):
        print(name) if name else ...
        print(self)
        if self.child:
            print('k l r p h s'.replace(' ', '\t'))
            self.child.printer()
            print('-' * 21)
        else:
            print('[]')


class Knot:

    def __init__(self, value, parent):
        self.key = value
        self.par = parent
        self.left = None
        self.right = None
        self.height = 1
        self.size = 1
        self.sum = ''
        self._div()

    def _div(self):
        if len(self.key) == 1:
            return

        m = len(self.key) // 2
        left, center, right = self.key[:m], self.key[m], self.key[m + 1:]
        self.left = Knot(left, parent=self) if left else None
        self.right = Knot(right, parent=self) if right else None
        self.key = center
        self.update(recur=False)

    def update_size(self):
        left = self.left.size if self.left else 0
        right = self.right.size if self.right else 0
        self.size = left + right + 1

    def update_sum(self):
        left = self.left.sum if self.left else ''
        right = self.right.sum if self.right else ''
        self.sum = left + self.key + right

    def update_height(self, recur=True):
        left = self.left.height if self.left else 0
        right = self.right.height if self.right else 0
        self.height = max(left, right) + 1

    def update(self, recur=True):
        self.update_height()
        self.rotation()
        self.update_size()
        # self.update_sum()
        if recur:
            self.par.update()

    def rotation(self):
        global i
        if self.how_right_higher() > 1:
            i += 1
            if self.right.how_right_higher() > 0:
                self.rotation_small_right()
            else:
                self.rotation_big_right()

            if self.right:
                self.right.par = self
                self.right.update_size()

        elif self.how_right_higher() < -1:
            i += 1
            if self.left.how_right_higher() <= 0:
                self.rotation_small_left()
            else:
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

    def add_next_brain(self, brain):
        if self.right:
            key = self.right.min()
            key.add_prev_brain(brain)
        else:
            self.right = brain
            if brain:
                brain.par = self
            self.update()

    def add_prev_brain(self, brain):
        key = self.min()
        key.left = brain
        if brain:
            brain.par = self
        key.update()

    def append(self, value):  # FIXME
        side = 'left' if value < self.key else 'right'
        if getattr(self, side) is None:
            setattr(self, side, Knot(value, parent=self))
            self.update()
        else:
            getattr(self, side).append(value)

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

        child.par = None
        self.update()

    def get_slice(self, start, end):
        out_left, res_left = self.split(start)
        if res_left:
            res_right, out_right = res_left.split(end-start)
            out = Avl.merge(out_left, out_right) if out_left else out_right
            return out, res_right
        return out_left, Avl()

    def split(self, i):
        left_size = self.left.size if self.left else 0
        if i == left_size:
            return Avl(child=self.left), Avl.merge_root(None, self.right, self.key)

        if i < left_size:
            if self.left:
                left, right = self.left.split(i)
                right = Avl.merge_root(right, self.right, self.key)
                return left, right
            else:
                return Avl(), Avl(child=self),

        else:
            if self.right:
                left, right = self.right.split(i - left_size - 1)
                left = Avl.merge_root(self.left, left, self.key)
                return left, right
            else:
                return Avl(child=self), Avl()

    def __str__(self):
        return ''.join(str(x) for x in (self.left, self.key, self.right) if not (x is None))

    def __repr__(self):
        return ('\t'.join((str(x.key) if x else '-') for x in (self, self.left, self.right, self.par))
                + '\t' + str(self.height)
                + '\t' + str(self.size)
                )

    def __getitem__(self, item):
        return self.get_i(item)

    def printer(self):
        self.left and self.left.printer()
        print(repr(self))
        self.right and self.right.printer()


if __name__ == '__main__':
    """
    cool = Avl('hlelowrold')
    cool.printer('main')

    key = cool.rope(1, 1, 2)
    key.printer('key1')
    key = key.rope(6, 6, 7)

    """
    # with sys.stdin as f:
    start = time.time()
    with open('1.txt') as f:
        text = f.readline().rstrip()
        avl = Avl(text)
        next(f)
        for line in f:
            i, j, k = [int(i) for i in line.split()]
            avl = avl.rope(i, j, k)
        print(avl)

    print(time.time() - start, 'i =', i)
