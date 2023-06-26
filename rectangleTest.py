import unittest

import rectangle


class RectangleTestCase(unittest.TestCase):
    def test_rectangle_create(self):
        """Test if the init method of rectangle is ok, by checking if all the attributes are assigned properly.
        """
        x = 5  # use case data
        y = 6
        w = 7
        h = 8
        rect = rectangle.Rectangle(x, y, w, h)
        self.assertEqual(rect.x, x)
        self.assertEqual(rect.y, y)
        self.assertEqual(rect.w, w)
        self.assertEqual(rect.h, h)

    def test_rectangle_contains(self):
        # TODO success and fail
        pass

    def test_rectangle_intersects(self):
        pass


if __name__ == '__main__':
    unittest.main()
