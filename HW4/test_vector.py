import os
from assembler import assembler, save_to_bin
from interpreter import interpreter

def generate_instructions():
    """Генерирует инструкции для выполнения операции сравнения < над вектором и числом 98."""
    instructions = []
    vector_a = [10, 20, 30, 40, 50, 60, 70]  # Вектор длины 7
    comparison_value = 98

    # Загрузка элементов первого вектора (A) в регистры и запись в память
    for i, value in enumerate(vector_a):
        instructions.append(("load_const", i, value))  # Загружаем в регистры 0-6
        instructions.append(("write_mem", i * 2, i))  # Записываем в память по адресам 0, 2, 4, 6, ...

    # Загрузка числа для сравнения (98) в регистр
    instructions.append(("load_const", len(vector_a), comparison_value))  # Загружаем число в регистр 7
    instructions.append(("write_mem", len(vector_a) * 2, len(vector_a)))  # Записываем в память по адресу 14

    # Выполнение операции сравнения < для каждого элемента
    for i in range(len(vector_a)):
        instructions.append(("read_mem", i * 2, i, 0))                 # Читаем элемент из памяти A
        instructions.append(("read_mem", len(vector_a) * 2, len(vector_a), 0))  # Читаем число для сравнения (98)
        instructions.append(("bin_op", i * 2 + 1, i * 2, len(vector_a) * 2))  # Сравниваем: A[i] < 98
        instructions.append(("write_mem", i * 2 + 2, i + len(vector_a)))      # Записываем результат в новый вектор
        
    return instructions

def write_yaml_instructions(instructions, file_path):
    """Сохраняет инструкции в yaml файл."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("operation,B,C\n")
        for instruction in instructions:
            f.write(",".join(map(str, instruction)) + "\n")

def main():
    # Параметры файлов
    instructions_file = "test_instructions.yaml"
    binary_file = "test_binary.bin"
    result_file = "test_result.yaml"  # Файл для записи результата
    log_file = "test_log.yaml"

    # Генерация инструкций
    instructions = generate_instructions()
    write_yaml_instructions(instructions, instructions_file)

    # Запуск ассемблера
    print("Сборка программы...")
    assembled_instructions = assembler(instructions, log_file)
    save_to_bin(assembled_instructions, binary_file)
    print(f"Программа собрана, бинарный файл: {binary_file}")

    # Запуск интерпретатора
    print("Запуск интерпретатора...")
    interpreter(binary_file, result_file, (0, 50))  # Убедимся, что обрабатываем всю память
    print(f"Результат интерпретации сохранён в файл: {result_file}")

if __name__ == "__main__":
    main()
