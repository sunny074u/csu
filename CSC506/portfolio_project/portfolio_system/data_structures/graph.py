from collections import deque
from typing import Any, Dict, List


class Graph:
    def __init__(self):
        self.adjacency: Dict[Any, List[Any]] = {}

    def add_vertex(self, vertex: Any) -> None:
        if vertex not in self.adjacency:
            self.adjacency[vertex] = []

    def add_edge(self, v1: Any, v2: Any) -> None:
        self.add_vertex(v1)
        self.add_vertex(v2)
        self.adjacency[v1].append(v2)
        self.adjacency[v2].append(v1)

    def bfs(self, start: Any) -> List[Any]:
        if start not in self.adjacency:
            return []

        visited = set()
        queue = deque([start])
        order = []

        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                order.append(vertex)
                for neighbor in self.adjacency[vertex]:
                    if neighbor not in visited:
                        queue.append(neighbor)

        return order

    def dfs(self, start: Any) -> List[Any]:
        if start not in self.adjacency:
            return []

        visited = set()
        stack = [start]
        order = []

        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                order.append(vertex)
                for neighbor in reversed(self.adjacency[vertex]):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return order

    def __str__(self) -> str:
        return str(self.adjacency)
