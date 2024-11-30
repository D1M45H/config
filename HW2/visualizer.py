import os
import yaml
from graphviz import Digraph

class DependencyVisualizer:
    def __init__(self, config):
        self.graphviz_path = config['graphviz_path']
        self.repo_path = config['repo_path']
        self.output_path = config['output_path']

    def get_dependencies(self):
        dependencies = {}
        
        # Получаем список всех коммитов из .git/refs/heads
        refs_path = os.path.join(self.repo_path, '.git', 'refs', 'heads')
        
        for branch in os.listdir(refs_path):
            branch_path = os.path.join(refs_path, branch)
            with open(branch_path, 'r') as f:
                commit_hash = f.read().strip()
                dependencies[commit_hash] = self.get_files_changed(commit_hash)

        return dependencies

    def get_files_changed(self, commit_hash):
        # Логика для получения измененных файлов в коммите
        changed_files = []
        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                changed_files.append(os.path.relpath(os.path.join(root, file), self.repo_path))
        return changed_files

    def generate_graph(self, dependencies):
        dot = Digraph(comment='Dependency Graph')

        for commit, files in dependencies.items():
            dot.node(commit, commit)
            for file in files:
                dot.node(file, file)
                dot.edge(commit, file)

        return dot

    def save_graph(self, dot):
        output_file = os.path.join(self.output_path, 'dependency_graph.png')
        dot.render(output_file, format='png', cleanup=True)  # Сохранение графа в PNG
        print(f"Граф зависимостей успешно сохранен в '{output_file}'")

    def visualize(self):
        dependencies = self.get_dependencies()
        dot = self.generate_graph(dependencies)
        self.save_graph(dot)

if __name__ == "__main__":
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    visualizer = DependencyVisualizer(config)
    visualizer.visualize()
