import unittest
from quadTree import Quadtree
from rectangle import Rectangle


class QuadTreeTestCase(unittest.TestCase):
    def load_usecase(self):
        """
        Load the common instances that will be used in several test cases.
        :return: None
        """
        self.boundary = Rectangle(5, 6, 70, 80)
        self.capacity = 4
        self.quadTree = Quadtree(self.boundary, self.capacity)

    def test_init(self):
        """
        Test if the properties of a quad tree are all assigned properly in the init method.
        :return: None
        """
        self.load_usecase()
        self.assertEqual(self.quadTree.boundary, self.boundary)
        self.assertEqual(self.quadTree.capacity, self.capacity)
        self.assertEqual(len(self.quadTree.rectangles), 0)
        self.assertFalse(self.quadTree.divided)

    def test_insert(self):
        # not intersects with the boundary
        # intersects with the boundary but not divided and not full
        # intersects with the boundary and divided
        # intersects with the boundary and full
        # TODO how to assert the result???
        pass

    def test_insert_into_children(self):
        pass

    def test_subdivide(self):
        pass

    def test_query_point(self):
        pass

    def test_draw(self):
        pass

    def test_remove(self):
        pass

    def test_move(self):
        pass


if __name__ == '__main__':
    unittest.main()
