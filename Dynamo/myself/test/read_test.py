import unittest
from readerdxf import FindDxf
from itemprop import Polygon


class TestFindDxf(unittest.TestCase):
    """Тест модуля по поиску Объектов в .dxf"""
    def setUp(self) -> None:
        """Считывание файла и поиск полигонов"""
        self.file = FindDxf('TestFindDxf.dxf')
        self.data_poly = self.file.find('LWPOLYLINE')

    def test_find_type(self):
        """Проверка функции find, что она возвращает список"""
        self.assertIsInstance(self.data_poly, list)

    def test_find_polyline_uni(self):
        """Проверка что возвращаются только полигоны"""
        data_type = set(map(type, self.data_poly))
        self.assertEqual(len(data_type), 1)

    def test_find_polyline_type(self):
        """Проверка что возвращаются именно полигоны"""
        data_type = list(set(map(type, self.data_poly)))[0]
        self.assertIs(data_type, Polygon)


if __name__ == '__main__':
    unittest.main()
