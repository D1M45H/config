import os
import subprocess
import yaml

class DependencyVisualizer:
    def __init__(self, config):
        self.graphviz_path = config['graphviz_path']
        self.repo_path = config['repo_path']
        self.output_path = config['output_path']

    def get_dependencies(self):
        os.chdir(self.repo_path)
        commits = subprocess.check_output(["git", "rev-list", "--all"]).decode().splitlines()
        dependencies = {}

        for commit in commits:
            files = subprocess.check_output(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit]).decode().splitlines()
            dependencies[commit] = files

        return dependencies

    def generate_graph(self, dependencies):
        graph = "digraph G {\n"
        
        for commit, files in dependencies.items():
            for file in files:
                graph += f'"{commit}" -> "{file}";\n'
        
        graph += "}"
        return graph

    def save_graph(self, graph):
        with open("graph.dot", "w") as f:
            f.write(graph)

        subprocess.run([self.graphviz_path, "-Tpng", "graph.dot", "-o", self.output_path])

    def visualize(self):
        dependencies = self.get_dependencies()
        graph = self.generate_graph(dependencies)
        self.save_graph(graph)
        print(f"Граф зависимостей успешно создан и сохранен в {self.output_path}")

if __name__ == "__main__":
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    visualizer = DependencyVisualizer(config)
    visualizer.visualize()
