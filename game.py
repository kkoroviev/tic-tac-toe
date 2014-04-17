from boards import TicTacToeBoard


class Game(object):
    def __init__(self, strategies):
        self.strategies = strategies
        self.board = TicTacToeBoard()
        self.me = 'X'
        self.you = 'O'
        self.interrupted = False

    def play(self, silent=False):
        game = self
        board = game.board

        while not (board.has_winner() or board.has_ended_in_draw() or game.interrupted):
            if not silent:
                self.display_board()
                self.display_prompt()

            try:
                x, y = self.strategies[self.me](game.board, self.me, self.you)
            except GameInterrupted:
                game.interrupted = True
                break

            if game.board.is_empty(x, y):
                game.board[(x, y)] = self.me
            else:
                raise RuntimeError("Your strategy `%s` wants to change non-empty cell (%s, %s). You shouldn't cheat!" %
                                   (self.strategies[self.me].__name__, x, y))

            # Swap players.
            self.me, self.you = self.you, self.me

        if not silent:
            self.display_outcome()

    def display_board(self):
        print
        print self.board.as_string(pretty=True)

    def display_prompt(self):
        print
        print "Your turn, %s." % self.human_readable_player_name(self.me)
        print "Where should I place your '%s'?" % self.me

    def human_readable_player_name(self, player):
        try:
            return {'X': "CROSS", 'O': "NOUGHT"}[player]
        except KeyError:
            raise ValueError("The `player` should be either 'X' or 'O'.")

    def display_outcome(self):
        game = self
        board = game.board

        if game.interrupted:
            print
            print "Player '%s' decided to quit." % self.me
            print
            return

        self.display_board()

        print
        if board.has_winner():
            print "Player '%s' wins." % board.winner()
            print
        elif board.has_ended_in_draw():
            print "It's a draw. Boring..."
            print
        else:
            # Should never happen.
            raise RuntimeError


class GameInterrupted(Exception):
    pass
