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

    def test_parse_value_simple(self):
        result = self.converter.parse_value('''
let max_users = 100;
let timeout = 30;
app_settings = [
    max_users,
    timeout
];
''')
        expected = '''
app_settings:
- 100
- 30
'''
        self.assertEqual(result.strip(), expected.strip())

    def test_parse_value_with_nested_arrays(self):
        result = self.converter.parse_value('''
let servers = [
    {"host": "localhost", "port": 8080},
    {"host": "example.com", "port": 80}
];
let max_connections = 200;
server_settings = [
    servers,
    max_connections
];
''')
        expected = '''
server_settings:
- - host: localhost
    port: 8080
  - host: example.com
    port: 80
- 200
'''
        self.assertEqual(result.strip(), expected.strip())

    def test_parse_value_with_mixed_types(self):
        result = self.converter.parse_value('''
let name = "MyApp";
let version = "1.0.0";
config = {
    app_name: name,
    app_version: version,
    features: [
        "feature1",
        "feature2"
    ]
};
''')
        expected = '''
config:
  app_name: MyApp
  app_version: 1.0.0
  features:
  - feature1
  - feature2
'''
        self.assertEqual(result.strip(), expected.strip())

if __name__ == '__main__':
    unittest.main()
