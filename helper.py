def _validate_maze(maze):
    if not maze or not maze[0]:
        raise ValueError("Maze must be a non-empty grid")
    cols = len(maze[0])
    for row in maze:
        if len(row) != cols:
            raise ValueError("Maze must be rectangular")


def find_positions(maze):
    _validate_maze(maze)
    start = None
    goal = None
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == "S":
                start = (i, j)
            elif cell == "G":
                goal = (i, j)
    if start is None or goal is None:
        raise ValueError("Maze must contain both 'S' and 'G'")
    return start, goal


def get_neighbors(maze, pos):
    rows = len(maze)
    cols = len(maze[0])
    row, col = pos
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = []

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < rows and 0 <= c < cols and maze[r][c] != "#":
            neighbors.append((r, c))

    return neighbors


def reconstruct_path(parent, start, goal):
    if start == goal:
        return [start]
    if goal not in parent:
        return None
    path = []
    curr = goal
    while curr != start:
        path.append(curr)
        curr = parent[curr]
    path.append(start)
    path.reverse()
    return path