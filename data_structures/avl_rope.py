from copy import deepcopy
import time


class Avl_text:
    def __init__(self, val=None, child=None):
        self.key = 'r'

        if val is None:
            self.child = child
            if child:
                child.par = self
        else:
            self.child = Node(val, parent=self)

    def min(self):
        if self.child is None:
            raise ValueError('min() arg is an empty sequence')
        return self.child.min()

    def max(self):
        if self.child is None:
            raise ValueError('max() arg is an empty sequence')
        return self.child.max()

    def split(self, i):
        return self.child.split(i)

    def split_slice(self, i, j):
        out_l, res = self.split(i)
        if res.child is None:
            return out_l, res
        res, out_r = res.split(j-i+1)
        if out_l.child is None and out_r.child is None:
            out = Avl_text(None)
        elif out_l.child is None or out_r.child is None:
            out = out_l if out_r.child is None else out_r
        else:
            out = out_l.merge(out_r)
        return out, res

    def rope(self, l, r, k):
        out, slice = self.split_slice(l, r)

        out.printer('out')
        slice.printer('slice')

        if k == 0:
            key = out.min()
            key.left = slice.child
            if slice.child is not None:
                slice.child.par = key
                slice.child.update()
        else:
            key = out.get_i(k)
            # print('~~~~', repr(key))
            key.new_brain(slice.child)

        return out

    def update(self):
        pass

    def new_child(self, old=None, new=None):
        self.child = new
        new.par = self

    def del_child(self, child):
        if self.child is child:
            self.child = None

        child.par = None

    def merge(self, other):
        one = self
        other = deepcopy(other)

        key = one.max()
        val = key.key
        key.delete()
        return self.merge_root(one.child, other.child, val)

    def get_i(self, i):
        if self.child is None:
            raise IndexError
        return self.child.get_i(i)

    @staticmethod
    def merge_root(left, right, key):
        if isinstance(left, Avl_text):
            left = left.child

        if isinstance(right, Avl_text):
            right = right.child

        new = Avl_text(key)
        new.child.left, new.child.right = deepcopy(left), deepcopy(right)
        if left:
            left.par = new.child
        if right:
            right.par = new.child
        new.child.update()

        return new

    def printer(self, name=''):
        print(name) if name else ...
        print(self)
        if self.child is None:
            print('[]')
        else:
            print('k l r p h s'.replace(' ', '---'))
            self.child.printer()
            print('-' * 21)

    def __str__(self):
        if self.child is None:
            return ''
        return str(self.child)


class Node:
    def __init__(self, val, parent=None):
        self.key = val
        self.par = parent
        self.left = None
        self.right = None
        self.height = 1
        self.size = len(val)
        if self.size > 1:
            self._div()

    def update(self, recur=True):
        self.update_height()
        self.rotation()
        self.update_size()

        if recur:
            self.par.update()

    def rotation(self):
        if self.how_right_higher() > 1:
            if self.right.how_right_higher() > 0:
                self.rotation_small_right()
            else:
                self.rotation_big_right()

            if self.right:
                self.right.par = self
                self.right.update_size()

        elif self.how_right_higher() < -1:
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

    def update_height(self):
        left = self.left.height if self.left else 0
        right = self.right.height if self.right else 0
        self.height = max(left, right) + 1

    def update_size(self):
        left = self.left.size if self.left else 0
        right = self.right.size if self.right else 0
        self.size = left + right + 1

    def _div(self):
        if len(self.key) == 1:
            return

        m = len(self.key) // 2
        left, center, right = self.key[:m], self.key[m], self.key[m+1:]
        self.left = Node(left, parent=self) if left else None
        self.right = Node(right, parent=self) if right else None
        self.key = center
        self.update(recur=False)

    def split(self, i):
        l_s = self.left.size if self.left else 0
        if i > l_s:
            if self.right:
                left, right = self.right.split(i-l_s-1)
                left = Avl_text.merge_root(self.left, left, self.key)
            else:
                left = Avl_text.merge_root(self.left, None, self.key)
                right = Avl_text(None, child=None)

        elif i < l_s:
            if self.left:
                left, right = self.left.split(i)
                right = Avl_text.merge_root(right, self.right, self.key)
            else:
                left = Avl_text(None, child=None)
                right = Avl_text.merge_root(None, self.right, self.key)

        else:  # i == l_s
            left = Avl_text(child=self.left)
            right = Avl_text.merge_root(None, self.right, self.key)

        return left, right

    def get_i(self, i):
        l_s = self.left.size if self.left else 0
        r_s = self.right.size if self.right else 0

        if l_s + 1 == i:
            return self
        elif i <= l_s:
            if self.left:
                return self.left.get_i(i)
            raise IndexError
        elif i > l_s:
            if self.right:
                return self.right.get_i(i-l_s-1)
            raise IndexError

    def new_brain(self, brain):
        if self.right is None:
            self.right = brain
            brain.par = self
        else:
            next_ = self.right.min()
            next_.left = brain
            brain.par = next_
        brain.update()

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

        while key.par.__class__ is not Avl_text:
            if key.par.left and key.par.left is key:
                return key.par
            key = key.par

        raise ValueError('don`t have next value')

    @staticmethod
    def prev_key(key):
        if key.left:
            return key.left.max()

        while key.par.__class__ is not Avl_text:
            if key.par.right and key.par.right is key:
                return key.par
            key = key.par

        raise ValueError('don`t have next value')

    def __repr__(self):
        return ('\t'.join((str(x.key) if x else '-') for x in (self, self.left, self.right, self.par))
                + '\t' + str(self.height)
                + '\t' + str(self.size)
                )

    def __str__(self):
        return ' '.join(str(x) for x in (self.left, self.key, self.right) if not (x is None))

    def printer(self):
        self.left and self.left.printer()
        print(repr(self))
        self.right and self.right.printer()


if __name__ == '__main__':
    cool = Avl_text('abcdef')
    cool.printer()

    one, two = cool.split(3)

    # one.printer('left')
    # two.printer('right')

    # out, slice = cool.split_slice(5, 9)
    # out.printer('out')
    # slice.printer('slice')

    fin = cool.rope(0, 1, 1)
    fin.printer('fin1')

    fin = fin.rope(4, 5, 0)
    fin.printer('fin2')


    # print(cool.get_i(9))