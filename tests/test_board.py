import unittest

from boards import Board


class TestEmptyBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_getitem(self):
        for x in xrange(3):
            for y in xrange(3):
                self.assertEqual(self.board[(x, y)], ' ')

    def test_setitem(self):
        for x in xrange(3):
            for y in xrange(3):
                self.board[(x, y)] = 'X'
                self.assertEqual(self.board[(x, y)], 'X')

    def test_out_of_bounds(self):
        for x in range(-2, 0) + range(3, 5):
            for y in range(-2, 0) + range(3, 5):
                with self.assertRaises(IndexError):
                    self.board[(x, y)] = 'X'

    def test_is_out_of_bounds(self):
        for x in range(-2, 0) + range(3, 5):
            for y in range(-2, 0) + range(3, 5):
                self.assertTrue(self.board.is_out_of_bounds(x, y))

    def test_iter(self):
        self.assertTrue(all(cell == ' ' for (coords, cell) in self.board))

    def test_contains(self):
        self.assertTrue(' ' in self.board)
        self.assertFalse('X' in self.board)
        self.assertFalse('O' in self.board)

    def test_is_empty(self):
        self.assertTrue(all(self.board.is_empty(x, y)
                            for x in xrange(3)
                            for y in xrange(3)))

    def test_is_occupied(self):
        self.assertFalse(any(self.board.is_occupied(x, y)
                             for x in xrange(3)
                             for y in xrange(3)))


class TestNearlyEmptyBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_is_empty(self):
        self.board[(0, 0)] = 'X'
        self.assertFalse(self.board.is_empty(0, 0))

    def test_is_occupied(self):
        self.board[(0, 0)] = 'X'
        self.assertTrue(self.board.is_occupied(0, 0))


class TestCornersSidesAndCenter(unittest.TestCase):
    def setUp(self):
        self.board = Board('\n'.join(['XOX',
                                      'O O',
                                      'XOX']))

    def test_corners(self):
        self.assertEqual(self.board.corners().values().count('X'), 4)

    def test_sides(self):
        self.assertEqual(self.board.sides().values().count('O'), 4)

    def test_center(self):
        self.assertEqual(self.board.center().values(), [' '])


class TestLines(unittest.TestCase):
    def setUp(self):
        self.board = Board('\n'.join(['XXX',
                                      'OOO',
                                      'ZZZ']))

    def test_horizontals(self):
        self.assertItemsEqual(self.board.horizontals().values(), (('X', 'X', 'X'),
                                                                  ('O', 'O', 'O'),
                                                                  ('Z', 'Z', 'Z')))

    def test_verticals(self):
        self.assertItemsEqual(self.board.verticals().values(), (('X', 'O', 'Z'),
                                                                ('X', 'O', 'Z'),
                                                                ('X', 'O', 'Z')))

    def test_diagonals(self):
        self.assertItemsEqual(self.board.diagonals().values(), (('X', 'O', 'Z'),
                                                                ('X', 'O', 'Z')))


class TestTextualRepresentation(unittest.TestCase):
    def setUp(self):
        self.text = ('''
XOX
O O
XOX
''')
        self.pretty_text = ('''
+---+
|XOX|
|O O|
|XOX|
+---+
''')
        self.board = Board(self.text)

    def test_as_string(self):
        self.assertEqual('\n%s\n' % self.board.as_string(), self.text)

    def test_as_pretty_string(self):
        self.assertEqual('\n%s\n' % self.board.as_string(pretty=True), self.pretty_text)


class TestOutOfBounds(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_getitem(self):
        for x in range(-2, 0) + range(3, 5):
            for y in range(-2, 0) + range(3, 5):
                with self.assertRaises(IndexError):
                    self.board[(x, y)]

    def test_setitem(self):
        for x in range(-2, 0) + range(3, 5):
            for y in range(-2, 0) + range(3, 5):
                with self.assertRaises(IndexError):
                    self.board[(x, y)] = 'X'


class TestOpposite(unittest.TestCase):
    def setUp(self):
        self.board = Board('''
123
456
789
''')

    def test_upper_left_and_lower_right_corners(self):
        coords = (0, 0)
        self.assertEqual(self.board[coords], '1')

        coords = self.board.opposite(*coords)
        self.assertEqual(self.board[coords], '9')

        coords = self.board.opposite(*coords)
        self.assertEqual(self.board[coords], '1')

    def test_upper_right_and_lower_left_corners(self):
        coords = (2, 0)
        self.assertEqual(self.board[coords], '3')

        coords = self.board.opposite(*coords)
        self.assertEqual(self.board[coords], '7')

        coords = self.board.opposite(*coords)
        self.assertEqual(self.board[coords], '3')

    def test_upper_and_lower_sides(self):
        coords = (1, 0)
        self.assertEqual(self.board[coords], '2')

        coords = self.board.opposite(*coords)
        self.assertEqual(self.board[coords], '8')

        coords = self.board.opposite(*coords)
        self.assertEqual(self.board[coords], '2')

    def test_left_and_right_sides(self):
        coords = (0, 1)
        self.assertEqual(self.board[coords], '4')

        coords = self.board.opposite(*coords)
        self.assertEqual(self.board[coords], '6')

        coords = self.board.opposite(*coords)
        self.assertEqual(self.board[coords], '4')

    def test_center(self):
        self.assertEqual((1, 1), self.board.opposite(1, 1))
