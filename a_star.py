import heapq

from helper import find_positions, get_neighbors, reconstruct_path


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(maze):
    start, goal = find_positions(maze)
    pq = [(heuristic(start, goal), start)]
    parent = {}
    g_cost = {start: 0}
    visited_order = []
    costs_info = {}

    while pq:
        f_val, current = heapq.heappop(pq)
        
        # Track the first time we visit a node (avoid duplicates from heapq)
        if current not in costs_info:
            costs_info[current] = {
                'f': f_val,
                'g': g_cost[current],
                'h': heuristic(current, goal)
            }
        
        if current in visited_order:
            continue
            
        visited_order.append(current)

        if current == goal:
            return reconstruct_path(parent, start, goal), visited_order, costs_info

        for neighbor in get_neighbors(maze, current):
            temp_g = g_cost[current] + 1

            if neighbor not in g_cost or temp_g < g_cost[neighbor]:
                g_cost[neighbor] = temp_g
                f_cost = temp_g + heuristic(neighbor, goal)
                heapq.heappush(pq, (f_cost, neighbor))
                parent[neighbor] = current

    return None, visited_order, costs_info