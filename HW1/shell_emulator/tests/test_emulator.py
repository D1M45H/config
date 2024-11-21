import unittest
import os
import zipfile

from emulator import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.zip_path = 'test_fs.zip'
        with zipfile.ZipFile(cls.zip_path, 'w') as zipf:
            zipf.writestr('test_dir/file1.txt', 'Hello World\nHello World\nGoodbye World\n')
            zipf.writestr('test_dir/file2.txt', 'Hello Again\nHello World\n')

        cls.script_path = 'test_script.sh'
        with open(cls.script_path, 'w') as f:
            f.write("ls\necho Hello\nuniq test_dir/file1.txt\ncd test_dir\nls\nexit\n")

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.zip_path)
        os.remove(cls.script_path)

    def setUp(self):
        self.emulator = ShellEmulator(self.zip_path, self.script_path)

    def test_ls(self):
        result = self.emulator.ls()
        self.assertIn('test_dir/file1.txt', result)
        self.assertIn('test_dir/file2.txt', result)

    def test_cd(self):
        self.emulator.cd('test_dir')
        self.assertEqual(self.emulator.current_dir, 'test_dir')

    def test_cd_invalid(self):
        with self.assertRaises(FileNotFoundError):
            self.emulator.cd('invalid_dir')

    def test_uniq(self):
        result = self.emulator.uniq('test_dir/file1.txt')
        expected_output = "Hello World\nGoodbye World"
        self.assertEqual(result, expected_output)

    def test_uniq_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            self.emulator.uniq('invalid_file.txt')

    def test_echo(self):
        result = self.emulator.echo("Hello", "World")
        self.assertEqual(result, "Hello World")

    def test_exit(self):
        try:
            self.emulator.exit()
            self.assertTrue(False) 
        except SystemExit:
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
