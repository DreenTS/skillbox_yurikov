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

    def test_not_enough_len(self):
        with self.assertRaises(bowling.FrameLengthError):
            bowling.get_score(game_result='X5/53629/9/')

    def test_wrong_char_set(self):
        with self.assertRaises(bowling.WrongCharSetError):
            bowling.get_score(game_result='8/5D9-X1Я5/50629/9/')

    def test_wrong_type(self):
        with self.assertRaises(bowling.WrongTypeError):
            bowling.get_score(124)
        with self.assertRaises(bowling.WrongTypeError):
            bowling.get_score(['124'])

    def test_wrong_value(self):
        with self.assertRaises(bowling.FrameSumError):
            bowling.get_score(game_result='8/599-XX5/57629/9/')
        with self.assertRaises(bowling.SpareError):
            bowling.get_score(game_result='8/549-XX-/53629/9/')
        with self.assertRaises(bowling.SpareError):
            bowling.get_score(game_result='/8549-XX5/53629/9/')


if __name__ == '__main__':
    unittest.main()
