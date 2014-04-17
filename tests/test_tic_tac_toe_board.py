import unittest

from boards import TicTacToeBoard


class TestCrossWins(unittest.TestCase):
    def setUp(self):
        self.board = TicTacToeBoard('''
XOO
XOO
XXX
''')

    def test_has_winner(self):
        self.assertTrue(self.board.has_winner())

    def test_winner(self):
        self.assertEqual(self.board.winner(), 'X')

    def test_has_ended_in_draw(self):
        self.assertFalse(self.board.has_ended_in_draw())


class TestNoughtWins(unittest.TestCase):
    def setUp(self):
        self.board = TicTacToeBoard('''
XOX
OOO
XOX
''')

    def test_has_winner(self):
        self.assertTrue(self.board.has_winner())

    def test_winner(self):
        self.assertEqual(self.board.winner(), 'O')

    def test_has_ended_in_draw(self):
        self.assertFalse(self.board.has_ended_in_draw())


class TestHasEndedInDraw(unittest.TestCase):
    def setUp(self):
        self.board = TicTacToeBoard('''
XOX
OOX
XXO
''')

    def test_has_winner(self):
        self.assertFalse(self.board.has_winner())

    def test_winner(self):
        self.assertIsNone(self.board.winner())

    def test_has_ended_in_draw(self):
        self.assertTrue(self.board.has_ended_in_draw())


class TestHasNotEndedInDrawYet(unittest.TestCase):
    def setUp(self):
        self.board = TicTacToeBoard('''
XOX
OOX
 XO
''')

    def test_has_winner(self):
        self.assertFalse(self.board.has_winner())

    def test_winner(self):
        self.assertIsNone(self.board.winner())

    def test_has_ended_in_draw(self):
        self.assertFalse(self.board.has_ended_in_draw())


class TestOnlyOneCanWin(unittest.TestCase):
    def setUp(self):
        self.board = TicTacToeBoard('''
OOO
XXX
 OX
''')

    def test_has_winner(self):
        self.assertRaises(RuntimeError, self.board.has_winner)

    def test_winner(self):
        self.assertRaises(RuntimeError, self.board.winner)

    def test_has_ended_in_draw(self):
        self.assertRaises(RuntimeError, self.board.has_ended_in_draw)
