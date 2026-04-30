import heapq

from helper import find_positions, get_neighbors, reconstruct_path


def ucs(maze):
    start, goal = find_positions(maze)
    pq = [(0, start)]
    visited = set()
    parent = {}
    cost_so_far = {start: 0}
    visited_order = []
    costs_info = {}

    while pq:
        cost, current = heapq.heappop(pq)
        
        if current not in costs_info:
            costs_info[current] = {'g': cost}
            
        if current not in visited_order:
            visited_order.append(current)

        if current == goal:
            return reconstruct_path(parent, start, goal), visited_order, costs_info

        if current in visited:
            continue
        visited.add(current)

        for neighbor in get_neighbors(maze, current):
            new_cost = cost + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor))
                parent[neighbor] = current

    return None, visited_order, costs_info