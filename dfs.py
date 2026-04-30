from helper import find_positions, get_neighbors, reconstruct_path


def dfs(maze):
    start, goal = find_positions(maze)
    stack = [(start, 0)]
    visited = {start}
    parent = {}
    visited_order = []
    costs_info = {}

    while stack:
        current, depth = stack.pop()
        visited_order.append(current)
        costs_info[current] = {'g': depth}

        if current == goal:
            return reconstruct_path(parent, start, goal), visited_order, costs_info

        for neighbor in get_neighbors(maze, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append((neighbor, depth + 1))

    return None, visited_order, costs_info