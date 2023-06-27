import unittest

from rectangle import Rectangle


class RectangleTestCase(unittest.TestCase):
    def test_rectangle_create(self):
        """Test if the init method of rectangle is OK, by checking if all the attributes are assigned properly.
        """
        x = 5  # use case data
        y = 6
        w = 7
        h = 8
        rect = Rectangle(x, y, w, h)
        self.assertEqual(rect.x, x)
        self.assertEqual(rect.y, y)
        self.assertEqual(rect.w, w)
        self.assertEqual(rect.h, h)

    def test_rectangle_contains(self):
        rect = Rectangle(3, 4, 20, 30)
        x_in, y_in = 5, 7
        x_on, y_on = 3, 13  # 23, 13 is not true, because the second operator is not <=
        x_out, y_out = 100, 300
        self.assertTrue(rect.contains(x_in, y_in))
        self.assertTrue(rect.contains(x_on, y_on))
        self.assertFalse(rect.contains(x_out, y_out))
        pass

    def test_rectangle_is_contained_in(self):
        """Test if the method is_contained_in() is OK.
        One is contained in, one is intersects, and one is not intersects and not contained in.
        """
        rect_out = Rectangle(0, 0, 40, 50)
        rect_in = Rectangle(2, 3, 5, 7)
        rect_not_in = Rectangle(33, 49, 20, 40)  # intersect but not contained
        rect_not_inter = Rectangle(44, 55, 10, 10)  # not intersect
        self.assertTrue(rect_in.is_contained_in(rect_out))
        self.assertFalse(rect_not_in.is_contained_in(rect_out))
        self.assertFalse(rect_not_inter.is_contained_in(rect_out))

    def test_rectangle_intersects(self):
        """Test if the method intersects() is OK.
        One is contained in, one is intersects, and one is not intersects and not contained in.
        Both way are tested.
        """
        rect_out = Rectangle(0, 0, 40, 50)
        rect_in = Rectangle(2, 3, 5, 7)  # contained in
        rect_inter = Rectangle(33, 49, 20, 40)  # intersect but not contained
        rect_not_inter = Rectangle(44, 55, 10, 10)  # not intersect
        self.assertTrue(rect_in.intersects(rect_out))
        self.assertTrue(rect_inter.intersects(rect_out))
        self.assertFalse(rect_not_inter.is_contained_in(rect_out))
        self.assertTrue(rect_out.intersects(rect_in))
        self.assertTrue(rect_out.intersects(rect_inter))
        self.assertFalse(rect_out.intersects(rect_not_inter))


if __name__ == '__main__':
    unittest.main()
