from collections import defaultdict

class DependencyGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.visited = set()
        self.order = []

    def add_dependency(self, dependent, dependency):
        self.graph[dependent].append(dependency)

    def topological_sort(self, node):
        self.visited.add(node)
        for dependency in self.graph[node]:
            if dependency not in self.visited:
                self.topological_sort(dependency)
        self.order.append(node)