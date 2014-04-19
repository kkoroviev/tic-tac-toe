import unittest

from strategies import strategy_human_parse


class TestStrategyHumanParse(unittest.TestCase):
    def test_strategy_human_parse(self):
        ret = strategy_human_parse('1, 1')
        self.assertEqual(ret, (0, 0))

    def test_wihout_spaces(self):
        ret = strategy_human_parse('2,3')
        self.assertEqual(ret, (1, 2))

    def test_a_lot_of_spaces(self):
        ret = strategy_human_parse('2,   \t5')
        self.assertEqual(ret, (1, 4))

    def test_no_comma(self):
        with self.assertRaises(ValueError):
            ret = strategy_human_parse('21')

    def test_more_than_one_comma(self):
        with self.assertRaises(ValueError):
            ret = strategy_human_parse('1,2,3')

    def test_no_numbers(self):
        with self.assertRaises(ValueError):
            ret = strategy_human_parse('middle, top')

    def test_leading_spaces(self):
        ret = strategy_human_parse('   2, 3')
        self.assertEqual(ret, (1, 2))

    def test_trailing_spaces(self):
        ret = strategy_human_parse('2, 3    ')
        self.assertEqual(ret, (1, 2))

    def test_multi_digit_numbers(self):
        ret = strategy_human_parse('100500, 1337')
        self.assertEqual(ret, (100499, 1336))
