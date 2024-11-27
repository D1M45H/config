import unittest
from config_converter import ConfigConverter

class TestConfigConverter(unittest.TestCase):

    def setUp(self):
        self.converter = ConfigConverter()

    def test_comment_1(self):
        self.converter.handle_constant_declaration("% test")
        self.assertEqual(result, "test")

    def test_comment_2(self):
        self.converter.handle_constant_declaration("(comment 1\n2")
        self.assertEqual(result, "1\n2")

    def test_constant_declaration(self):
        self.converter.handle_constant_declaration("let test_var = 5;")
        self.assertEqual(self.converter.constants['test_var'], 5)

    def test_array_parsing(self):
        result = self.converter.parse_array("[[1, 2], 3]")
        self.assertEqual(result, [[1, 2], 3])

    def test_expression_evaluation(self):
        self.converter.handle_constant_declaration("let a = {- 10 2};")
        result = self.converter.evaluate_expression("{+ a 5}")
        self.assertEqual(result, 13)

    def test_expression_evaluation_abs(self):
        result = self.converter.evaluate_expression("{abs -5}")
        self.assertEqual(result, 5)

if __name__ == '__main__':
    unittest.main()
