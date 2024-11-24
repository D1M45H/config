import argparse
import re
import yaml

class ConfigConverter:
    def __init__(self):
        self.constants = {}

    def parse_file(self, input_file):
        with open(input_file, 'r') as file:
            lines = file.readlines()
        
        return self.parse_lines(lines)

    def parse_lines(self, lines):
        result = {}
        current_key = None
        
        for line in lines:
            line = line.strip()
            if self.is_comment(line):
                continue
            elif self.is_constant_declaration(line):
                self.handle_constant_declaration(line)
            elif self.is_array(line):
                current_key = self.extract_key(line)
                result[current_key] = self.parse_array(line)
            elif self.is_value(line):
                current_key = self.extract_key(line)
                result[current_key] = self.parse_value(line)
            elif self.is_expression(line):
                value = self.evaluate_expression(line)
                result[current_key] = value
            else:
                raise SyntaxError(f"Неизвестный синтаксис: {line}")
        
        return result

    def is_comment(self, line):
        return line.startswith('%') or line.startswith('(comment')

    def is_constant_declaration(self, line):
        return re.match(r'let [a-z]+ = .+;', line)

    def handle_constant_declaration(self, line):
        match = re.match(r'let ([a-z]+) = (.+);', line)
        if match:
            name, value = match.groups()
            self.constants[name] = self.parse_value(value)

    def is_array(self, line):
        return line.startswith('[') and line.endswith(']')

    def parse_array(self, line):
        array_content = line[1:-1].strip()
        values = [self.parse_value(value.strip()) for value in array_content.split(',')]
        return values

    def is_value(self, line):
        return re.match(r'[a-z]+ = .+;', line)

    def extract_key(self, line):
        return re.match(r'([a-z]+) =', line).group(1)

    def parse_value(self, value):
        if value.isdigit():
            return int(value)
        elif re.match(r'^[a-z]+$', value):
            return self.constants.get(value, value)
        elif self.is_array(value):
            return self.parse_array(value)
        else:
            raise ValueError(f"Некорректное значение: {value}")

    def is_expression(self, line):
        return line.startswith('{') and line.endswith('}')

    def evaluate_expression(self, expression):
        expr_content = expression[1:-1].strip()
        parts = expr_content.split()
        operator = parts[0]
        args = [self.constants.get(arg, arg) for arg in parts[1:]]

        if operator == '+':
            return sum(int(arg) for arg in args)
        elif operator == '-':
            return int(args[0]) - sum(int(arg) for arg in args[1:])
        elif operator == 'abs':
            return abs(int(args[0]))
        else:
            raise ValueError(f"Неизвестная операция: {operator}")

def main():
    parser = argparse.ArgumentParser(description='Конвертер конфигурационного языка в YAML.')
    parser.add_argument('--input', required=True, help='Путь к входному файлу')
    parser.add_argument('--output', required=True, help='Путь к выходному файлу')
    
    args = parser.parse_args()

    converter = ConfigConverter()
    try:
        result = converter.parse_file(args.input)
        with open(args.output, 'w') as output_file:
            yaml.dump(result, output_file)
    except SyntaxError as e:
        print(f"Синтаксическая ошибка: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
