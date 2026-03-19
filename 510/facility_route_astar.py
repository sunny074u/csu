"""
Informed Search (A*) with SimpleAI on a grid-based "facility route planning" problem.

Legend:
  S = Start
  G = Goal
  . = normal tile (cost 1)
  M = slow tile (cost 5) 
  W = blocked tile  
  * = path found by A*

Requires:
  pip install simpleai==0.8.2   (0.8.3 should also work)

Run:
  python facility_route_astar.py
"""

from __future__ import annotations

from typing import List, Tuple, Optional, Iterable

from simpleai.search import SearchProblem, astar


Coord = Tuple[int, int]

DEFAULT_MAP = [
    "S...W....",
    ".W..W.M..",
    ".W..W....",
    ".W.......",
    "...MMM.W.",
    "W....W.W.",
    "....W....",
    "..M..W..G",
]

# Movement costs (cost is paid when you ENTER a tile)
COSTS = {
    ".": 1,
    "S": 1,
    "G": 1,
    "M": 5,  # slow zone
}

BLOCKED = {"W"}  # cannot traverse


def parse_coord(text: str, rows: int, cols: int) -> Coord:
    """
    Parse 'row,col' into a validated coordinate.
    Example: 7, 8
    """
    parts = text.strip().split(",")
    if len(parts) != 2:
        raise ValueError("Enter coordinates as row,col (example: 0,0)")
    r = int(parts[0].strip())
    c = int(parts[1].strip())
    if not (0 <= r < rows and 0 <= c < cols):
        raise ValueError(f"Out of bounds. row in [0,{rows-1}], col in [0,{cols-1}]")
    return (r, c)


def find_symbol(grid: List[str], symbol: str) -> Optional[Coord]:
    for r, line in enumerate(grid):
        for c, ch in enumerate(line):
            if ch == symbol:
                return (r, c)
    return None


def printable_grid(grid: List[str]) -> str:
    return "\n".join(grid)


def overlay_path(grid: List[str], path_coords: Iterable[Coord]) -> List[str]:
    """
    Overlay '*' on path coords (excluding S and G).
    """
    g = [list(row) for row in grid]
    for (r, c) in path_coords:
        if g[r][c] not in ("S", "G"):
            g[r][c] = "*"
    return ["".join(row) for row in g]


class FacilityRouteProblem(SearchProblem):
    """
    State: (row, col)
    Actions: U, D, L, R
    Cost: based on the tile you move into ('.'=1, 'M'=5)
    Heuristic: Manhattan distance * min_step_cost
    """

    def __init__(self, initial_state: Coord, grid: List[str], goal: Coord, min_step_cost: int = 1):
        # SimpleAI stores initial_state in the base class
        super().__init__(initial_state=initial_state)
        self.grid = tuple(grid)
        self.goal = goal
        self.min_step_cost = min_step_cost

    def actions(self, state: Coord) -> List[str]:
        r, c = state
        candidates = [
            ("U", (r - 1, c)),
            ("D", (r + 1, c)),
            ("L", (r, c - 1)),
            ("R", (r, c + 1)),
        ]

        rows = len(self.grid)
        cols = len(self.grid[0]) if rows else 0

        valid: List[str] = []
        for action, (nr, nc) in candidates:
            if 0 <= nr < rows and 0 <= nc < cols:
                tile = self.grid[nr][nc]
                if tile not in BLOCKED:
                    valid.append(action)
        return valid

    def result(self, state: Coord, action: str) -> Coord:
        r, c = state
        if action == "U":
            return (r - 1, c)
        if action == "D":
            return (r + 1, c)
        if action == "L":
            return (r, c - 1)
        if action == "R":
            return (r, c + 1)
        raise ValueError(f"Unknown action: {action}")

    def is_goal(self, state: Coord) -> bool:
        return state == self.goal

    def cost(self, state: Coord, action: str, state2: Coord) -> int:
        r2, c2 = state2
        tile = self.grid[r2][c2]
        if tile in BLOCKED:
            # Should never happen because actions() filters it out.
            return 10**9
        return COSTS.get(tile, 1)

    def heuristic(self, state: Coord) -> int:
        r, c = state
        gr, gc = self.goal
        manhattan = abs(r - gr) + abs(c - gc)
        # Multiply by the minimum possible step cost to keep it admissible
        return manhattan * self.min_step_cost


def summarize_solution(result_node):
    """
    Extract coordinates, actions, and total cost from a SimpleAI result node.
    result_node.path() returns:
      [(None, initial_state), (action1, state1), (action2, state2), ...]
    """
    path = result_node.path()
    coords = [st for (_act, st) in path]  # includes initial and goal
    actions = [act for (act, _st) in path if act is not None]
    total_cost = getattr(result_node, "cost", None)
    if total_cost is None:
        total_cost = len(actions)
    return coords, actions, int(total_cost)


def main() -> None:
    grid = DEFAULT_MAP[:]  # copy
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    start = find_symbol(grid, "S")
    goal = find_symbol(grid, "G")
    if start is None or goal is None:
        raise RuntimeError("Map must include both 'S' and 'G'.")

    print("\n=== Facility Route Planner (A*) ===\n")
    print("Map legend: S=start, G=goal, .=cost1, M=cost5, W=blocked\n")
    print(printable_grid(grid))
    print("\nCurrent start:", start, "goal:", goal)

    # Optional user override
    choice = input("\nUse default S/G from the map? (Y/n): ").strip().lower()
    if choice == "n":
        try:
            start = parse_coord(input("Enter start as row,col: "), rows, cols)
            goal = parse_coord(input("Enter goal  as row,col: "), rows, cols)

            if grid[start[0]][start[1]] in BLOCKED:
                raise ValueError("Start is on a blocked tile (W). Pick another.")
            if grid[goal[0]][goal[1]] in BLOCKED:
                raise ValueError("Goal is on a blocked tile (W). Pick another.")
        except Exception as e:
            print(f"\nInput error: {e}\nUsing default S/G from the map.")
            start = find_symbol(grid, "S")
            goal = find_symbol(grid, "G")

    problem = FacilityRouteProblem(
        initial_state=start,
        grid=grid,
        goal=goal,
        min_step_cost=1,
    )

    print("\nSearching with A* (graph_search=True) ...")
    result = astar(problem, graph_search=True)

    if result is None:
        print("\nNo route found (goal unreachable from start).")
        return

    coords, actions, total_cost = summarize_solution(result)
    routed = overlay_path(grid, coords)

    print("\n=== Result ===")
    print("Actions:", " ".join(actions))
    print("Steps:", len(actions))
    print("Total cost:", total_cost)

    # Extra debugging/visibility (nice for grading)
    if hasattr(result, "depth"):
        print("Node depth:", result.depth)
    if hasattr(result, "cost"):
        print("Node cost :", result.cost)

    print("\nPath overlay:\n")
    print(printable_grid(routed))
    print("\nDone.\n")


if __name__ == "__main__":
    main()