import argparse
import yaml

# Функция для записи логов операции
def log_operation(log_path, operation_code, *args):
    if log_path is not None:
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"A={operation_code},B={args[0]},C={args[1]}\n")

# Функция сериализации команды в бинарный формат
def serializer(cmd, fields, size):
    bits = 0
    bits |= cmd  # Устанавливаем код операции в младшие биты
    for value, offset in fields:
        bits |= (value << offset)  # Добавляем операнды в соответствующие биты
    return bits.to_bytes(size, "little")

# Основная функция ассемблера
def assembler(instructions, log_path=None):
    byte_code = []
    for operation, *args in instructions:
        if operation == "load_const":
            B, C = args
            # Команда "Загрузка константы" - A=9, B=Адрес, C=Константа
            byte_code += serializer(9, ((B, 4), (C, 15)), 6)
            log_operation(log_path, 9, B, C)
        elif operation == "read_mem":
            B, C, D = args
            # Команда "Чтение значения из памяти" - A=15, B=Адрес, C=Адрес D=Смещение
            byte_code += serializer(15, ((B, 4), (C, 15), (D, 26)), 6)
            log_operation(log_path, 15, B, C, D)
        elif operation == "write_mem":
            B, C = args
            # Команда "Запись значения в память" - A=7, B=Адрес, C=Адрес
            byte_code += serializer(7, ((B, 4), (C, 15)), 6)
            log_operation(log_path, 7, B, C)
        elif operation == "bin_op":
            B, C, D = args
            # Команда "Бинарная операция: <" - A=14, B=Адрес, C=Адрес, D=Адрес
            byte_code += serializer(4, ((B, 4), (C, 15), (D, 26)), 6)
            log_operation(log_path, 4, B, C, D)
    return byte_code

# Функция для чтения инструкций из yaml файла и их сборки
def assemble(instructions_path: str, log_path=None):
    instructions = []
    with open(instructions_path, "r", encoding="utf-8") as f:
        reader = yaml.safe_load(f)
        for row in reader:
            operation = row[0].strip()
            args = [int(x) if x.isdigit() else x for x in row[1:]]
            instructions.append([operation] + args)
    return assembler(instructions, log_path)

# Сохранение бинарных данных в файл
def save_to_bin(assembled_instructions, binary_path):
    with open(binary_path, "wb") as binary_file:
        binary_file.write(bytes(assembled_instructions))

# Главная точка входа
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembling the instructions yaml file to the byte-code.")
    parser.add_argument("instructions_path", help="Path to the instructions yaml file")
    parser.add_argument("binary_path", help="Path to the binary file (bin)")
    parser.add_argument("log_path", help="Path to the log file (yaml)")
    args = parser.parse_args()
    
    # Создание лог файла
    with open(args.log_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"Operation code,Constant/Address,Address\n")
    
    # Ассемблирование инструкций и сохранение в бинарный файл
    result = assemble(args.instructions_path, args.log_path)
    save_to_bin(result, args.binary_path)