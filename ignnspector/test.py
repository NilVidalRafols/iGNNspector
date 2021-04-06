from analysis import analyzer
import unittest   # The test framework

class Test_Analyzer(unittest.TestCase):
    def test_increment(self):
        self.assertEqual(1+2, 4)

    def test_decrement(self):
        self.assertEqual(4-0, 4)

if __name__ == '__main__':
    unittest.main()