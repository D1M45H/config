import struct
import sys
import yaml

class UVM:
    def __init__(self):
        self.memory = [0] * 1024
        self.result = {}

    def load_program(self, binary_file):
        with open(binary_file, 'rb') as f:
            self.program = f.read()

    def run(self):
        pc = 0
        while pc < len(self.program):
            instruction = self.program[pc:pc + 6]
            A, B, C, D = struct.unpack('>BHHH', instruction)

            if A == 0xD:  # LOAD_CONST
                self.memory[B] = C
            elif A == 0xF:  # READ_MEM
                address = self.memory[C] + D
                self.memory[B] = self.memory[address]
            elif A == 0x7:  # WRITE_MEM
                self.memory[C] = self.memory[B]
            elif A == 0x4:  # BINARY_OP_LT
                first_operand = self.memory[self.memory[D]]
                second_operand = self.memory[C]
                self.memory[B] = int(first_operand < second_operand)

            pc += 6

    def save_results(self, output_file):
        with open(output_file, 'w') as f:
            yaml.dump(self.memory, f)

if __name__ == "__main__":
    binary_file = sys.argv[1]
    output_file = sys.argv[2]
    
    uvm = UVM()
    uvm.load_program(binary_file)
    uvm.run()
    uvm.save_results(output_file)
