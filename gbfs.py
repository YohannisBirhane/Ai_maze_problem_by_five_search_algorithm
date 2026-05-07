import heapq

from helper import find_positions, get_neighbors, reconstruct_path


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def greedy(maze):
    start, goal = find_positions(maze)
    pq = [(heuristic(start, goal), start)]
    visited = set()
    parent = {}
    visited_order = []
    costs_info = {}

    while pq:
        h_val, current = heapq.heappop(pq)
        
        if current not in costs_info:
            costs_info[current] = {'h': h_val}
            
        if current in visited:
            continue
        visited.add(current)
        
        visited_order.append(current)

        if current == goal:
            return reconstruct_path(parent, start, goal), visited_order, costs_info

        for neighbor in get_neighbors(maze, current):
            if neighbor not in visited:
                parent[neighbor] = current
                heapq.heappush(pq, (heuristic(neighbor, goal), neighbor))

    return None, visited_order, costs_info

if __name__ == "__main__":
    test_maze = [
        ["S", ".", ".", "#"],
        ["#", ".", "#", "."],
        [".", ".", ".", "G"],
    ]
    path, visited, costs = greedy(test_maze)
    print("Greedy Path:", path)
    print("Nodes Visited:", len(visited))
