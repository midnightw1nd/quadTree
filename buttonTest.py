import unittest
from button import Button


class ButtonTestCase(unittest.TestCase):
    def load_usecase(self):
        """
        Load the common instances which are used in multiple test cases.
        """
        self.x = 5
        self.y = 6
        self.w = 7
        self.h = 8
        self.text = "test text"
        self.button = Button(self.x, self.y, self.w, self.h, self.text)

    def test_init(self):
        """
        Test if the properties are properly assigned in the init method.
        :return: None
        """
        self.load_usecase()
        self.assertEqual(self.button.rect.x, self.x)
        self.assertEqual(self.button.rect.y, self.y)
        self.assertEqual(self.button.rect.w, self.w)
        self.assertEqual(self.button.rect.h, self.h)
        self.assertEqual(self.button.text, self.text)

    def test_draw(self):  # I don't know how to test.
        pass

    def test_is_over(self):
        """
        Test if the is_over() method is running properly.
        One spot on the edge, one spot far away, and one spot inside.
        :return: None
        """
        self.load_usecase()
        x_col, y_col = 5, 8
        x_not_col, y_not_col = 1, 2.2
        x_in, y_in = 6, 7.7
        self.assertTrue(self.button.is_over((x_col, y_col)))
        self.assertFalse(self.button.is_over((x_not_col, y_not_col)))
        self.assertTrue(self.button.is_over((x_in, y_in)))


if __name__ == '__main__':
    unittest.main()
