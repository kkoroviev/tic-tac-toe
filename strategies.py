import copy
from functools import wraps

from game import GameInterrupted


########################################################################
#                                                                      #
#  Decorators                                                          #
#                                                                      #
########################################################################

def print_strategy_choice(f):
    @wraps(f)
    def wrapper(board, me, you):
        x, y = f(board, me, you)
        print '%s: %s, %s' % (me, x, y)
        return (x, y)
    return wrapper

def should_return_list(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return list(f(*args, **kwargs))
    return wrapper


########################################################################
#                                                                      #
#  `strategy_dumb`                                                     #
#                                                                      #
########################################################################

@print_strategy_choice
def strategy_dumb(board, me, you):
    for ((x, y), cell) in board:
        if board.is_empty(x, y):
            return (x, y)


########################################################################
#                                                                      #
#  `strategy_human`                                                    #
#                                                                      #
########################################################################

def strategy_human(board, me, you):
    while True:
        print
        print "Type your choice ('x, y'; 1 <= (x, y) <= 3), or 'q<Enter>' to exit."

        # No new line after the prompt.
        print "%s:" % me,

        try:
            user_input = raw_input()
        except (EOFError, KeyboardInterrupt):
            # We don't have <CR> after the prompt.
            # We should add one.
            print
            raise GameInterrupted

        # Someone can be stupid enough to interpret 'q<Enter>' literally...
        if user_input.lower() in ('q', 'q<enter>'):
            # Here user typed <CR> for us already.
            raise GameInterrupted

        try:
            x, y = strategy_human_parse(user_input)
        except (TypeError, ValueError):
            continue

        # First, check if `(x, y)` are in bounds.
        # Otherwise, you can get `KeyError`,
        # when you try to call `is_occupied()`.
        if board.is_out_of_bounds(x, y):
            print
            # Use "human-readable" coords.
            print "Cell (%s, %s) doesn't exist, choose existing one." % (x + 1, y + 1)
            continue

        if board.is_occupied(x, y):
            print
            # Use "human-readable" coords.
            print "Cell (%s, %s) is occupied, choose another one." % (x + 1, y + 1)
            continue

        return (x, y)

def strategy_human_parse(user_input):
    try:
        x, y = map(int, user_input.split(',', 1))
    except (ValueError, TypeError):
        raise ValueError("Got nonsense instead of user input: %s.", repr(user_input))

    # Return "computer-readable" coords.
    return (x - 1, y - 1)


########################################################################
#                                                                      #
#  `strategy_never_lose`                                               #
#                                                                      #
########################################################################

@print_strategy_choice
def strategy_never_lose(board, me, you):
    actions = [try_to_win,
               dont_give_them_to_win,
               try_to_fork,
               prevent_their_fork,
               play_center,
               play_opposite_corner,
               play_empty_corner,
               anything_goes]
    for action in actions:
        try:
            x, y = action(board, me, you)
        except TypeError as e:
            if e.message == "'NoneType' object is not iterable":
                continue
            else:
                raise
        else:
            return x, y

    # Should never happen.
    raise RuntimeError

def try_to_win(board, me, you):
    wins = get_possible_wins(board, me, you)
    return wins[0] if wins else None

@should_return_list
def get_possible_wins(board, me, you):
    for ((x, y), cell) in board:
        if cell == ' ':
            new_board = copy.deepcopy(board)
            new_board[(x, y)] = me
            if new_board.winner() == me:
                yield (x, y)

def dont_give_them_to_win(board, me, you):
    return try_to_win(board, you, me)

def try_to_fork(board, me, you):
    for ((x, y), cell) in board:
        if cell == ' ':
            new_board = copy.deepcopy(board)
            new_board[(x, y)] = me
            if len(get_possible_wins(new_board, me, you)) > 1:
                return (x, y)
    return None

def prevent_their_fork(board, me, you):
    return try_to_fork(board, you, me)

def play_center(board, me, you):
    return (1, 1) if board.is_empty(1, 1) else None

def play_opposite_corner(board, me, you):
    your_corners = {coords: cell
                    for (coords, cell) in board.corners().items()
                    if cell == you}
    if len(your_corners) == 1:
        x, y = your_corners.keys()[0]
        return board.opposite(x, y)
    else:
        return None

def play_empty_corner(board, me, you):
    for ((x, y), cell) in board.corners().iteritems():
        if cell == ' ':
            return (x, y)
    return None

def anything_goes(board, me, you):
    for ((x, y), cell) in board:
        if cell == ' ':
            return (x, y)
