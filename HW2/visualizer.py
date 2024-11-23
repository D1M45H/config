import os
import subprocess
import yaml
import git
from collections import defaultdict

class DependencyVisualizer:
    def __init__(self, config):
        self.graphviz_path = config['graphviz_path']
        self.repo_path = config['repo_path']
        self.output_file = config['output_file']
        self.repo = git.Repo(self.repo_path)
        self.dependencies = defaultdict(set)

    def get_commit_dependencies(self):
        for commit in self.repo.iter_commits():
            for entry in commit.tree.traverse():
                if entry.type in ['blob', 'tree']:
                    self.dependencies[commit.hexsha].add(entry.path)

    def generate_graph(self):
        dot_content = "digraph G {\n"
        
        for commit, files in self.dependencies.items():
            for file in files:
                dot_content += f'    "{commit}" -> "{file}";\n'
        
        dot_content += "}\n"
        
        with open("graph.dot", "w") as f:
            f.write(dot_content)

        return self.create_png()

    def create_png(self):
        try:
            subprocess.run([self.graphviz_path, "-Tpng", "graph.dot", "-o", self.output_file], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating PNG: {e}")
            return False

    def visualize(self):
        self.get_commit_dependencies()
        if self.generate_graph():
            print(f"Graph successfully created and saved to {self.output_file}.")
        else:
            print("Failed to create graph.")

if __name__ == "__main__":
    with open("config.yaml", 'r') as f:
        config = yaml.safe_load(f)

    visualizer = DependencyVisualizer(config)
    visualizer.visualize()