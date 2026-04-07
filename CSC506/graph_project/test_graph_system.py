from __future__ import annotations

from adjacency_matrix_graph import AdjacencyMatrixGraph
from adjacency_list_graph import AdjacencyListGraph


SAMPLE_EDGES = [
    ("A", "B", 2),
    ("A", "C", 5),
    ("B", "D", 1),
    ("B", "E", 4),
    ("C", "F", 2),
    ("D", "E", 1),
    ("D", "G", 7),
    ("E", "F", 3),
    ("E", "H", 6),
    ("F", "H", 1),
    ("G", "H", 2),
]


def build_sample_graph(graph):
    for source, target, weight in SAMPLE_EDGES:
        graph.add_edge(source, target, weight)
    return graph


def ascii_visual() -> str:
    lines = [
        "               G",
        "              / \\",
        "             7   2",
        "            /     \\",
        "A --2-- B --1-- D --1-- E --3-- F --1-- H",
        "\\      |        \\                /",
        " 5      4         \\6            /",
        "  \\    |          \\          /",
        "    C --2----------- F --------",
    ]
    return "\n" + "\n".join(lines) + "\n"


def run_demo(graph, label: str) -> None:
    print("=" * 80)
    print(label)
    print("=" * 80)
    build_sample_graph(graph)

    print("\nGraph structure")
    if hasattr(graph, "display_matrix"):
        print(graph.display_matrix())
        print()
    print(graph.display_connections())

    print("\nVisual sketch of the sample graph")
    print(ascii_visual())

    print("\nDFS traversal from A")
    dfs_order = graph.depth_first_search("A", show_steps=True)
    print(f"DFS order: {dfs_order}")

    print("\nBFS traversal from A")
    bfs_order = graph.breadth_first_search("A", show_steps=True)
    print(f"BFS order: {bfs_order}")

    print("\nShortest path from A to H")
    cost, path = graph.shortest_path("A", "H", show_steps=True)
    print(f"Best route from A to H: {path} | total cost = {cost}")

    print("\nManipulation test")
    graph.add_vertex("I")
    graph.add_edge("H", "I", 2)
    print("Added vertex I and edge H-I")
    print(graph.display_connections())
    graph.remove_edge("H", "I")
    graph.remove_vertex("I")
    print("Removed edge H-I and vertex I")
    print(graph.display_connections())
    print()


if __name__ == "__main__":
    run_demo(AdjacencyMatrixGraph(directed=False), "Adjacency Matrix Graph Demo")
    run_demo(AdjacencyListGraph(directed=False), "Adjacency List Graph Demo")
