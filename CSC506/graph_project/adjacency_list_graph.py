from __future__ import annotations

from collections import deque
import heapq
from typing import Any, Dict, List, Optional, Set, Tuple


class AdjacencyListGraph:
    """
    Graph implementation backed by an adjacency list.

    Features:
    - supports directed or undirected graphs
    - supports weighted edges (default weight = 1)
    - add/remove vertices and edges
    - DFS and BFS with step-by-step output
    - Dijkstra shortest path for weighted graphs
    - display helpers for adjacency list view
    """

    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self.adjacency: Dict[Any, Dict[Any, float]] = {}

    def __len__(self) -> int:
        return len(self.adjacency)

    def _validate_vertex(self, vertex: Any) -> None:
        if vertex not in self.adjacency:
            raise ValueError(f"Vertex {vertex!r} does not exist in the graph.")

    @property
    def vertices(self) -> List[Any]:
        return list(self.adjacency.keys())

    def add_vertex(self, vertex: Any) -> None:
        if vertex not in self.adjacency:
            self.adjacency[vertex] = {}

    def remove_vertex(self, vertex: Any) -> None:
        self._validate_vertex(vertex)
        self.adjacency.pop(vertex)
        for source in self.adjacency:
            self.adjacency[source].pop(vertex, None)

    def add_edge(self, source: Any, target: Any, weight: float = 1) -> None:
        self.add_vertex(source)
        self.add_vertex(target)
        self.adjacency[source][target] = weight
        if not self.directed:
            self.adjacency[target][source] = weight

    def remove_edge(self, source: Any, target: Any) -> None:
        self._validate_vertex(source)
        self._validate_vertex(target)
        self.adjacency[source].pop(target, None)
        if not self.directed:
            self.adjacency[target].pop(source, None)

    def has_edge(self, source: Any, target: Any) -> bool:
        self._validate_vertex(source)
        self._validate_vertex(target)
        return target in self.adjacency[source]

    def get_neighbors(self, vertex: Any) -> List[Tuple[Any, float]]:
        self._validate_vertex(vertex)
        return list(self.adjacency[vertex].items())

    def display_connections(self) -> str:
        lines = []
        for vertex in self.vertices:
            neighbors = self.get_neighbors(vertex)
            if neighbors:
                joined = ", ".join(f"{nbr}({wt})" for nbr, wt in neighbors)
            else:
                joined = "No connections"
            lines.append(f"{vertex} -> {joined}")
        return "\n".join(lines)

    def depth_first_search(self, start: Any, show_steps: bool = True) -> List[Any]:
        self._validate_vertex(start)
        visited: Set[Any] = set()
        order: List[Any] = []

        def dfs(vertex: Any, depth: int = 0) -> None:
            visited.add(vertex)
            order.append(vertex)
            if show_steps:
                print(f"DFS visit: {vertex} | depth={depth} | path_so_far={order}")
            for neighbor, _ in self.get_neighbors(vertex):
                if neighbor not in visited:
                    if show_steps:
                        print(f"  DFS explore edge {vertex} -> {neighbor}")
                    dfs(neighbor, depth + 1)
                elif show_steps:
                    print(f"  DFS skip visited edge {vertex} -> {neighbor}")

        dfs(start)
        return order

    def breadth_first_search(self, start: Any, show_steps: bool = True) -> List[Any]:
        self._validate_vertex(start)
        visited: Set[Any] = {start}
        queue: deque[Any] = deque([start])
        order: List[Any] = []

        while queue:
            vertex = queue.popleft()
            order.append(vertex)
            if show_steps:
                print(f"BFS visit: {vertex} | queue={list(queue)} | visited={sorted(visited, key=str)}")
            for neighbor, _ in self.get_neighbors(vertex):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    if show_steps:
                        print(f"  BFS enqueue: {neighbor} via {vertex}")
                elif show_steps:
                    print(f"  BFS skip visited edge {vertex} -> {neighbor}")
        return order

    def shortest_path(self, start: Any, goal: Any, show_steps: bool = True) -> Tuple[float, List[Any]]:
        self._validate_vertex(start)
        self._validate_vertex(goal)

        distances: Dict[Any, float] = {vertex: float("inf") for vertex in self.vertices}
        previous: Dict[Any, Optional[Any]] = {vertex: None for vertex in self.vertices}
        distances[start] = 0
        pq: List[Tuple[float, Any]] = [(0, start)]

        while pq:
            current_distance, current_vertex = heapq.heappop(pq)
            if current_distance > distances[current_vertex]:
                continue
            if show_steps:
                print(f"Dijkstra pick: {current_vertex} | current_distance={current_distance}")
            if current_vertex == goal:
                break

            for neighbor, weight in self.get_neighbors(current_vertex):
                candidate_distance = current_distance + weight
                if show_steps:
                    print(
                        f"  Check edge {current_vertex} -> {neighbor} (weight={weight}) | "
                        f"candidate={candidate_distance} | known={distances[neighbor]}"
                    )
                if candidate_distance < distances[neighbor]:
                    distances[neighbor] = candidate_distance
                    previous[neighbor] = current_vertex
                    heapq.heappush(pq, (candidate_distance, neighbor))
                    if show_steps:
                        print(f"    Update: best path to {neighbor} now costs {candidate_distance}")

        if distances[goal] == float("inf"):
            return float("inf"), []

        path: List[Any] = []
        cursor: Optional[Any] = goal
        while cursor is not None:
            path.append(cursor)
            cursor = previous[cursor]
        path.reverse()

        if show_steps:
            print(f"Shortest path result: cost={distances[goal]} | path={path}")
        return distances[goal], path


if __name__ == "__main__":
    graph = AdjacencyListGraph(directed=False)
    for node in ["A", "B", "C", "D", "E"]:
        graph.add_vertex(node)
    graph.add_edge("A", "B", 2)
    graph.add_edge("A", "C", 4)
    graph.add_edge("B", "D", 3)
    graph.add_edge("C", "D", 1)
    graph.add_edge("D", "E", 5)

    print("Adjacency List")
    print(graph.display_connections())
    print("\nDFS from A")
    print(graph.depth_first_search("A"))
    print("\nBFS from A")
    print(graph.breadth_first_search("A"))
    print("\nShortest Path A -> E")
    print(graph.shortest_path("A", "E"))
