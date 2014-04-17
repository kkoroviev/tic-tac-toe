class Board(object):
    def __init__(self, text=None):
        self._data = list(text.replace('\n', '')) if text else [' '] * 9

    def corners(self):
        return {(x, y): self[(x, y)]
                for (x, y) in [(0, 0), (2, 0), (0, 2), (2, 2)]}

    def sides(self):
        return {(x, y): self[(x, y)]
                for (x, y) in [(1, 0), (0, 1), (2, 1), (1, 2)]}

    def center(self):
        return {(1, 1): self[(1, 1)]}

    def horizontals(self):
        keys = tuple(tuple((x, y) for x in xrange(3))
                     for y in xrange(3))
        return {key: tuple(self[coords] for coords in key)
                for key in keys}

    def verticals(self):
        keys = tuple(tuple((x, y) for y in xrange(3))
                     for x in xrange(3))
        return {key: tuple(self[coords] for coords in key)
                for key in keys}

    def diagonals(self):
        keys = (tuple((x, x) for x in xrange(3)),
                tuple((2 - x, x) for x in xrange(3)))
        return {key: tuple(self[coords] for coords in key)
                for key in keys}

    def __getitem__(self, key):
        x, y = key
        if self.is_out_of_bounds(x, y):
            raise IndexError
        return self._data[y * 3 + x]

    def __setitem__(self, key, value):
        x, y = key
        if self.is_out_of_bounds(x, y):
            raise IndexError
        self._data[y * 3 + x] = value

    def is_out_of_bounds(self, x, y):
        return not self.is_in_bounds(x, y)

    def is_in_bounds(self, x, y):
        return ((0 <= x <= 2) and (0 <= y <= 2))

    def __iter__(self):
        return iter(((x, y), self[x, y]) for y in xrange(3) for x in xrange(3))

    def __contains__(self, item):
        return item in self._data

    def as_string(self, pretty = False):
        lines = []
        for y in xrange(3):
            lines.append(''.join(self[(x, y)] for x in xrange(3)))
        if pretty:
            lines = [('|%s|' % line) for line in lines]
            bar = '+---+'
            lines.append(bar)
            lines.insert(0, bar)
        return '\n'.join(lines)

    def is_occupied(self, x, y):
        return self[(x, y)] != ' '

    def is_empty(self, x, y):
        return not self.is_occupied(x, y)

    def opposite(self, x, y):
        return (2 - x, 2 - y)


class TicTacToeBoard(Board):
    def has_winner(self):
        return self.winner() is not None

    def winner(self):
        board = self

        cross_wins = 0
        nought_wins = 0

        for line in board.verticals().values() + board.horizontals().values() + board.diagonals().values():
            if line.count('X') == 3:
                cross_wins += 1
            if line.count('O') == 3:
                nought_wins += 1

        if cross_wins != 0 and nought_wins != 0:
            raise RuntimeError("Both players can't win simultaneously!")
            # By the way, it is possible (in theory)
            # for `cross_wins` to be equal to 2:
            #
            # +---+
            # |XOO|
            # |XOO|
            # |XXX|
            # +---+
            #
            # Here you can clearly see two lines
            # (1 vertical and 1 horizontal)
            # entirely occupied by crosses.

        return 'X' if (cross_wins != 0) else 'O' if (nought_wins != 0) else None

    def has_ended_in_draw(self):
        return not self.has_winner() and ' ' not in self
