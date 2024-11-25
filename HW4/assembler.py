import struct
import sys
import yaml

def assemble(input_file, output_file, log_file):
    instruction_set = {
        'LOAD_CONST': 0xD,
        'READ_MEM': 0xF,
        'WRITE_MEM': 0x7,
        'BINARY_OP_LT': 0x4
    }
    
    instructions = []
    log = {}

    with open(input_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            
            op = parts[0]
            if op not in instruction_set:
                raise ValueError(f"Unknown operation: {op}")

            A = instruction_set[op]
            B = int(parts[1])
            C = int(parts[2])
            D = int(parts[3]) if len(parts) > 3 else 0

            if op == 'LOAD_CONST':
                instruction = struct.pack('>BHHH', A, B, C, 0)
            elif op == 'READ_MEM':
                instruction = struct.pack('>BHHH', A, B, C, D)
            elif op == 'WRITE_MEM':
                instruction = struct.pack('>BHHH', A, B, C, 0)
            elif op == 'BINARY_OP_LT':
                instruction = struct.pack('>BHHH', A, B, C, D)

            instructions.append(instruction)
            log[f"{op} A={A} B={B} C={C} D={D}"] = instruction.hex()

    with open(output_file, 'wb') as f:
        for instruction in instructions:
            f.write(instruction)

    with open(log_file, 'w') as f:
        yaml.dump(log, f)

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]
    assemble(input_file, output_file, log_file)
