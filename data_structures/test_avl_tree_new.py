from unittest import TestCase
from avl_tree_new import Avl
import random


class TestAvl(TestCase):
    def setUp(self) -> None:
        self.avl = Avl()
        self.one = random.randint(0, 10 ** 3)

        n = 100
        self.data = list({random.randint(-10 ** 3, 10 ** 3) for _ in range(n)})
        self.data_out = ' '.join(str(x) for x in sorted(self.data))

    def test_append_small(self):
        self.avl.append(self.one)
        self.assertEqual(str(self.avl), str(self.one))

    def test_append_large(self):
        for val in self.data:
            self.avl.append(val)
        self.assertEqual(str(self.avl), self.data_out)

    def test_extend_list(self):
        self.avl.extend(self.data)
        self.assertEqual(str(self.avl), self.data_out)

    def test_find_small(self):
        self.avl.append(self.one)
        out = self.avl.find(self.one)
        self.assertEqual(out.key, self.one)

    def test_find_large(self):
        self.avl.extend(self.data)
        k = random.choice(self.data)
        out = self.avl.find(k)
        self.assertEqual(out.key, k)

    def test_find_nothing(self):
        self.avl.extend(self.data)
        k = random.randint(-10 ** 3, 10 ** 3)
        while k in self.data:
            k = random.randint(-10 ** 3, 10 ** 3)

        with self.assertRaises(KeyError):
            self.avl.find(k)

    def test_min(self):
        self.avl.extend(self.data)
        out = self.avl.min()
        self.assertEqual(out.key, min(self.data))

    def test_min_nothing(self):
        with self.assertRaises(ValueError):
            self.avl.min()

    def test_max(self):
        self.avl.extend(self.data)
        out = self.avl.max()
        self.assertEqual(out.key, max(self.data))

    def test_max_nothing(self):
        with self.assertRaises(ValueError):
            self.avl.max()

    def test_reload_height_append(self):
        self.avl.extend([5, 3, 6])
        self.assertEqual(self.avl.child.height, 2)

    def test_next_val(self):
        self.avl.extend(self.data)
        self.data.sort()
        i = random.randint(0, len(self.data) - 2)  # -2, так как исключаем максимум
        out = self.avl.next_val(self.data[i])
        self.assertEqual(out.key, self.data[i + 1])

    def test_next_val_max(self):
        self.avl.extend(list(set(self.data)))
        with self.assertRaises(ValueError):
            self.avl.next_val(max(self.data))

    def test_prev_val(self):
        self.avl.extend(self.data)
        self.data.sort()
        i = random.randint(1, len(self.data) - 1)  # 1, так как исключаем минимум
        out = self.avl.prev_val(self.data[i])
        self.assertEqual(out.key, self.data[i - 1])

    def test_prev_val_min(self):
        self.avl.extend(list(set(self.data)))
        with self.assertRaises(ValueError):
            self.avl.prev_val(min(self.data))

    def test_delete_val(self):
        self.avl.extend(self.data)
        key = random.choice(self.data)
        self.avl.delete_val(key)
        self.assertEqual(str(self.avl).split().count(str(key)), self.data.count(key)-1)

    def test_delete_val_root(self):
        self.avl.append(12)
        self.avl.delete_val(12)
        self.assertEqual(str(self.avl), '')

    def test_delete_nothing(self):
        self.avl.extend(self.data)
        k = random.randint(-10 ** 3, 10 ** 3)
        while k in self.data:
            k = random.randint(-10 ** 3, 10 ** 3)

        with self.assertRaises(KeyError):
            self.avl.delete_val(k)

    def test_delete_knot_last(self):
        self.avl.extend([5, 3, 6])
        self.avl.delete_val(3)
        self.assertIsNone(self.avl.find(5).left)

    def test_delete_knot_penult(self):  # penult переводится, как предпоследний
        self.avl.extend([5, 3, 6, 1])
        self.avl.delete_val(3)
        self.assertIs(self.avl.find(5).left, self.avl.find(1))
        self.assertIs(self.avl.find(1).par, self.avl.find(5))

    def test_delete_knot_usual(self):
        self.avl.extend([5, 3, 6, 1, 4])
        self.avl.delete_val(3)
        self.assertIs(self.avl.find(5).left, self.avl.find(4))
        self.assertIs(self.avl.find(4).left, self.avl.find(1))
        self.assertIs(self.avl.find(1).par, self.avl.find(4))

    def test_reload_height_delete(self):
        self.avl.extend([5, 3, 6, 1])
        self.avl.delete_val(3)
        self.assertEqual(self.avl.find(5).height, 2)

    def test_rotation_small_right(self):
        self.avl.extend([30, 50, 70])
        self.assertIs(self.avl.child, self.avl.find(50))
        self.assertEqual(self.avl.find(50).height, 2)
        self.assertEqual(self.avl.find(30).height, 1)

    def test_rotation_big_right(self):
        self.avl.extend([30, 50, 40])
        self.assertIs(self.avl.child, self.avl.find(40))
        self.assertEqual(self.avl.find(40).height, 2)
        self.assertEqual(self.avl.find(30).height, 1)

    def test_rotation_small_left(self):
        self.avl.extend([30, 20, 10])
        self.assertIs(self.avl.child, self.avl.find(20))
        self.assertEqual(self.avl.find(20).height, 2)
        self.assertEqual(self.avl.find(30).height, 1)

    def test_rotation_big_left(self):
        self.avl.extend([30, 20, 25])
        self.assertIs(self.avl.child, self.avl.find(25))
        self.assertEqual(self.avl.find(25).height, 2)
        self.assertEqual(self.avl.find(30).height, 1)

    def test_get_i(self):
        self.avl.extend(self.data)
        self.data.sort()
        self.assertEqual(self.avl[5].key, self.data[5])

    def test_get_i_negative(self):
        self.avl.extend(self.data)
        self.data.sort()
        self.assertEqual(self.avl[-5].key, self.data[-5])

    def test_get_i_out(self):
        self.avl.extend(self.data)
        with self.assertRaises(IndexError):
            _ = self.avl[len(self.data) + 10]

    def test_len(self):
        self.avl.extend(self.data)
        self.assertEqual(len(self.avl), len(self.data))

    def test_len_empty(self):
        self.assertEqual(len(self.avl), 0)

    def test_contains_true(self):
        self.avl.extend(self.data)
        k = random.choice(self.data)
        self.assertTrue(k in self.avl)

    def test_contains_false(self):
        self.avl.extend(self.data)
        k = random.randint(-10 ** 3, 10 ** 3)
        while k in self.data:
            k = random.randint(-10 ** 3, 10 ** 3)
        self.assertFalse(k in self.avl)

    def test_merge_root(self):
        one = Avl([1, 2, 3])
        two = Avl([5, 6, 7])
        self.assertEqual(str(one.merge(two)), '1 2 3 5 6 7')

    def test_merge_left(self):
        one = Avl(list(range(0, 3)))
        two = Avl(list(range(10, 20)))
        new = one.merge(two)
        self.assertEqual(new.child.left.key, 2)

    def test_merge_right(self):
        one = Avl(list(range(0, 11)))
        two = Avl(list(range(18, 22)))
        new = one.merge(two)
        self.assertEqual(new.child.right.key, 19)

    def test_merge_random(self):
        data_one = [random.randint(-10**4, 0) for _ in range(random.randint(3, 100))]
        data_two = [random.randint(1, 10**4) for _ in range(random.randint(3, 100))]
        data_out = ' '.join(str(i) for i in (sorted(data_one) + sorted(data_two)))

        one = Avl(data_one)
        two = Avl(data_two)
        self.assertEqual(str(one.merge(two)), data_out)
