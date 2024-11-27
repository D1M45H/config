import unittest
from visualizer import DependencyVisualizer

class TestDependencyVisualizer(unittest.TestCase):
    def setUp(self):
        self.config = {
            'graphviz_path': '/usr/bin/dot',
            'repo_path': 'my_repo',
            'output_file': 'dependences.png'
        }
        self.visualizer = DependencyVisualizer(self.config)

    def test_get_commit_dependencies(self):
        self.visualizer.get_dependencies()
        self.assertGreater(len(self.visualizer.dependencies), 0)

    def test_generate_graph(self):
        self.visualizer.get_dependencies()
        result = self.visualizer.generate_graph()
        self.assertTrue(result)

    def test_create_png(self):
        self.visualizer.get_dependencies()
        self.visualizer.generate_graph()
        result = self.visualizer.save_graph()
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
