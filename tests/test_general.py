from analysis import analyzer
import unittest   # The test framework

class Test_GraphReport(unittest.TestCase):
    def test_init(self):
        r = GraphReport()
    
    def test_init_file(self):
        contents = {}
        contents['name'] = 'Reddit'
        content['num_edges'] = '24'
        content['num_edges'] = '56'

        with open('graph_report_file_1.txt', 'r') as f:
            report = GraphReport(f)
            self.assertEqual(report.contents, contents)

class Test_Analyzer(unittest.TestCase):
    def test_increment(self):
        self.assertEqual(1+2, 4)

    def test_decrement(self):
        self.assertEqual(4-0, 4)

class Test_Proposer(unittest.TestCase)

if __name__ == '__main__':
    unittest.main()