import unittest
from config_converter import ConfigConverter

class TestConfigConverter(unittest.TestCase):

    def setUp(self):
        self.converter = ConfigConverter()

    def test_single_line_comment(self):
        lines = [
            "% Это однострочный комментарий\n"
        ]
        result = self.converter.parse_lines(lines)
        self.assertEqual(result, {})

    def test_multiline_comment(self):
        lines = [
            "(comment\n",
            "Это многострочный\n",
            "комментарий\n",
            ")\n"
        ]
        result = self.converter.parse_lines(lines)
        self.assertEqual(result, {})

    def test_constant_declaration(self):
        lines = ["let x = 42;\n"]
        self.converter.parse_lines(lines)
        self.assertEqual(self.converter.constants, {"x": 42})

    def test_array_parsing(self):
        result = self.converter.parse_array("[1, 2, 3]")
        self.assertEqual(result, [1, 2, 3])

    def test_nested_array(self):
        result = self.converter.parse_array("[[1, 2], 3]")
        self.assertEqual(result, [[1, 2], 3])

    def test_expression_evaluation(self):
        self.converter.handle_constant_declaration("let a = 10;")
        result = self.converter.evaluate_expression("{+ a 5}")
        self.assertEqual(result, 15)

    def test_expression_subtraction(self):
        self.converter.handle_constant_declaration("let b = 20;")
        result = self.converter.evaluate_expression("{- b 5}")
        self.assertEqual(result, 15)

    def test_expression_abs(self):
        result = self.converter.evaluate_expression("{abs -15}")
        self.assertEqual(result, 15)


    
if __name__ == '__main__':
    unittest.main()
