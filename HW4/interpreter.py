import argparse

def popcnt(value):
    """Подсчет количества установленных битов (единиц) в числе."""
    return bin(value).count('1')

def interpreter(binary_path, result_path, memory_range):
    # Инициализация памяти и регистров
    memory = [0] * 64  # 64 ячейки памяти
    registers = [0] * 32  # 32 регистра (предполагается)

    with open(binary_path, "rb") as binary_file:
        byte_code = binary_file.read()

    i = 0
    while i < len(byte_code):
        command = byte_code[i] & 0x0F  # Биты 0-3 для команды
        
        if command == 9:  # load_const (Загрузка константы)
            B = (int.from_bytes(byte_code[i:i+6], "little") >> 4) & 0x1F  # Адрес
            C = (int.from_bytes(byte_code[i:i+6], "little") >> 15) & 0xFFFFF  # Константа
            memory[B] = C  # Результат: значение в памяти по адресу B
            print(f"Загрузка константы: память[{B}] = {C}")

        elif command == 15:  # read_mem (Чтение значения из памяти)
            B = (int.from_bytes(byte_code[i:i+6], "little") >> 4) & 0x1F  # Адрес для записи результата
            C = (int.from_bytes(byte_code[i:i+6], "little") >> 15) & 0xFFFFF  # Адрес для чтения
            D = (int.from_bytes(byte_code[i:i+6], "little") >> 26) & 0x3F  # Смещение
            
            address_to_read = memory[C] + D
            if 0 <= address_to_read < len(memory):  # Проверка диапазона
                memory[B] = memory[address_to_read]  # Результат: значение по адресу B
                print(f"Чтение из памяти: память[{B}] = память[{address_to_read}]")

        elif command == 7:  # write_mem (Запись значения в память)
            B = (int.from_bytes(byte_code[i:i+6], "little") >> 4) & 0x3F  # Адрес для чтения
            C = (int.from_bytes(byte_code[i:i+6], "little") >> 15) & 0x1F  # Адрес для записи
            memory[C] = memory[B]  # Результат: значение по адресу C
            print(f"Запись в память: память[{C}] = память[{B}]")

        elif command == 4:  # bin_op (<)
            B = (int.from_bytes(byte_code[i:i+6], "little") >> 4) & 0x3F  # Адрес для записи результата
            C = (int.from_bytes(byte_code[i:i+6], "little") >> 15) & 0x1F  # Второй операнд
            D = (int.from_bytes(byte_code[i:i+6], "little") >> 26) & 0x3F  # Первый операнд
            
            first_operand_address = memory[D]  # Значение по адресу D
            second_operand_value = memory[C]    # Значение по адресу C
            
            if first_operand_address < len(memory):  
                memory[B] = memory[first_operand_address] < second_operand_value
                print(f"Бинарная операция '<': память[{B}] = память[{first_operand_address}] < память[{C}]")

        i += 6  # Переход к следующей команде (каждая команда занимает 6 байт)

    # Запись значений в файл-результат
    with open(result_path, "w", encoding="utf-8") as result_file:
        result_file.write("Address,Value\n")
        for address in range(memory_range[0], memory_range[1] + 1):
            if 0 <= address < len(memory):  # Проверка диапазона адресов
                result_file.write(f"{address},{memory[address]}\n")
                print(f"Память[{address}] = {memory[address]}")
            else:
                print(f"Ошибка: Адрес {address} выходит за пределы памяти.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpreting the bytes like instructions (from binary file) to the csv-table.")
    parser.add_argument("binary_path", help="Path to the binary file (bin)")
    parser.add_argument("result_path", help="Path to the result file (yaml)")
    parser.add_argument("first_index", help="The first index of the displayed memory")
    parser.add_argument("last_index", help="The last index of the displayed memory")
    args = parser.parse_args()
    interpreter(args.binary_path, args.result_path, (int(args.first_index), int(args.last_index)))
