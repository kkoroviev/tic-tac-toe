import unittest

from strategies import strategy_human_parse


class TestStrategyHumanParse(unittest.TestCase):
    def test_strategy_human_parse(self):
        ret = strategy_human_parse('1, 1')
        self.assertEqual(ret, (0, 0))
