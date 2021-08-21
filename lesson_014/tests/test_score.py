import unittest
import bowling


class ScoreTest(unittest.TestCase):

    def test_normal(self):
        result = bowling.get_score(game_result='8/549-XX5/53629/9/')
        self.assertEqual(result, 134)
        result = bowling.get_score(game_result='1163718/72627/X8-7/')
        self.assertEqual(result, 109)
        result = bowling.get_score(game_result='x1235---616-9xx-7')
        self.assertEqual(result, 100)


if __name__ == '__main__':
    unittest.main()
