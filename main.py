from a_star import astar
from bfs import bfs
from dfs import dfs
from gbfs import greedy
from ucs import ucs


def format_path(path):
    if not path:
        return "No path"
    return " -> ".join(f"({r},{c})" for r, c in path)


def run_all(maze):
    algorithms = [
        ("BFS", bfs),
        ("DFS", dfs),
        ("UCS", ucs),
        ("Greedy", greedy),
        ("A*", astar),
    ]

    for name, func in algorithms:
        result = func(maze)
        if isinstance(result, tuple):
            path, _ = result
        else:
            path = result
        print(f"{name}: {format_path(path)}")


if __name__ == "__main__":
    maze = [
        ["S", ".", ".", "#"],
        ["#", ".", "#", "."],
        [".", ".", ".", "G"],
    ]

    run_all(maze)
