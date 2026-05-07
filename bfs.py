from collections import deque

from helper import find_positions, get_neighbors, reconstruct_path


def bfs(maze):
    start, goal = find_positions(maze)
    queue = deque([(start, 0)]) # (position, depth/cost)
    visited = {start}
    parent = {}
    visited_order = []
    costs_info = {}

    while queue:
        current, depth = queue.popleft()
        visited_order.append(current)
        
        costs_info[current] = {'g': depth}

        if current == goal:
            return reconstruct_path(parent, start, goal), visited_order, costs_info

        for neighbor in get_neighbors(maze, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append((neighbor, depth + 1))

    return None, visited_order, costs_info

if __name__ == "__main__":
    test_maze = [
        ["S", ".", ".", "#"],
        ["#", ".", "#", "."],
        [".", ".", ".", "G"],
    ]
    path, visited, costs = bfs(test_maze)
    print("BFS Path:", path)
    print("Nodes Visited:", len(visited))
