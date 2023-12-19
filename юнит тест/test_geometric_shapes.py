import unittest
from geometric_shapes import Triangle, Rectangle


class TestGeometricShapes(unittest.TestCase):
    def test_triangle_area(self):
        triangle = Triangle()
        self.assertEqual(triangle.area(3, 4 , 5 ), 6.0)

    def test_rectangle_area(self):
        rectangle = Rectangle()
        self.assertEqual(rectangle.area(5, 4), 20.0)


unittest.main()
