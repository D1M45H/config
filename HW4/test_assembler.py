from assembler import assembler

def test_load_const():
    instructions = [
        ("load_const", 109, 365)  # Пример: Загрузка константы
    ]
    expected_bytes = bytes([0xD9, 0x86, 0xB6, 0x00, 0x00, 0x00])
    result = assembler(instructions)
    assert result == list(expected_bytes), f"Test load_const failed. Expected {expected_bytes}, got {bytes(result)}"
    print("Test load_const passed.")

def test_read_mem():
    instructions = [
        ("read_mem", 609, 162, 256)  # Пример: Чтение значения из памяти
    ]
    expected_bytes = bytes([0x1F, 0x26, 0x51, 0x00, 0x04, 0x00])
    result = assembler(instructions)
    assert result == list(expected_bytes), f"Test read_mem failed. Expected {expected_bytes}, got {bytes(result)}"
    print("Test read_mem passed.")

def test_write_mem():
    instructions = [
        ("write_mem", 425, 985)  # Пример: Запись значения в память
    ]
    expected_bytes = bytes([0x97, 0x9A, 0xEC, 0x01, 0x00, 0x00])
    result = assembler(instructions)
    assert result == list(expected_bytes), f"Test write_mem failed. Expected {expected_bytes}, got {bytes(result)}"
    print("Test write_mem passed.")

def test_bin_op():
    instructions = [
        ("bin_op", 145, 931, 418)  # Пример: Бинарная операция (взятие остатка)
    ]
    expected_bytes = bytes([0x14, 0x89, 0xD1, 0x89, 0x06, 0x00])
    result = assembler(instructions)
    assert result == list(expected_bytes), f"Test bin_op failed. Expected {expected_bytes}, got {bytes(result)}"
    print("Test bin_op passed.")

if __name__ == "__main__":
    test_load_const()
    test_read_mem()
    test_write_mem()
    test_bin_op()
    print("All tests passed successfully!")