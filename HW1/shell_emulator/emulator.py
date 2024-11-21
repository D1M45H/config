import os
import sys
import zipfile

class ShellEmulator:
    def __init__(self, zip_path, script_path):
        self.zip_path = zip_path
        self.script_path = script_path
        self.current_dir = '/'
        self.file_system = {}
        self.load_file_system()
        self.commands = {
            'ls': self.ls,
            'cd': self.cd,
            'exit': self.exit,
            'uniq': self.uniq,
            'echo': self.echo
        }
        self.run_script()

    def load_file_system(self):
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                self.file_system[file] = zip_ref.read(file).decode('utf-8')

    def ls(self):
        return [file for file in self.file_system if os.path.dirname(file) == self.current_dir]

    def cd(self, path):
        if path == '..':
            self.current_dir = os.path.dirname(self.current_dir)
        elif any(file.startswith(path + '/') for file in self.file_system):
            self.current_dir = path
        else:
            raise FileNotFoundError(f"cd: {path}: No such file or directory")

    def uniq(self, filename):
        if filename not in self.file_system:
            raise FileNotFoundError(f"uniq: {filename}: No such file")
        
        lines = set(self.file_system[filename].splitlines())
        return "\n".join(lines)

    def echo(self, *args):
        return " ".join(args)

    def exit(self):
        sys.exit(0)

    def run_script(self):
        if not os.path.exists(self.script_path):
            print(f"Script {self.script_path} not found.")
            return
        
        with open(self.script_path, 'r') as script_file:
            for line in script_file:
                command_parts = line.strip().split()
                command = command_parts[0]
                args = command_parts[1:]
                if command in self.commands:
                    try:
                        output = self.commands[command](*args)
                        if output is not None:
                            print(output)
                    except Exception as e:
                        print(e)
                else:
                    print(f"{command}: command not found")

def main():
    if len(sys.argv) != 3:
        print("Usage: python emulator.py <path_to_zip> <path_to_script>")
        sys.exit(1)

    emulator = ShellEmulator(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
