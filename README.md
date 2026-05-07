# AI Pathfinding in a Maze

A Python project demonstrating and comparing five fundamental Artificial Intelligence search algorithms solving a 2D grid maze problem. The project features both command-line outputs and interactive graphical user interfaces (GUIs) to visualize how each algorithm explores the map.

## 🎯 The Maze Problem
Given a 2D grid maze, an AI agent must navigate from the **Start (S)** to the **Goal (G)**.
- **`.`** represents an open traversable path.
- **`#`** represents a wall or an obstacle.
- The cost to move to any adjacent cell (up, down, left, right) is exactly `1`.
- The AI cannot pass through walls.

The core objective is to analyze how different pathfinding algorithms arrive at the goal, comparing their optimality (finding the shortest path) and memory/time efficiency.

---

## 🧠 Searching Algorithms Implemented

### 1. Breadth-First Search (BFS)
* **Concept:** Explores equally in all directions, expanding layer by layer (like a water ripple).
* **Data Structure:** Queue (FIFO).
* **Characteristics:** Guarantees the shortest path (Optimal) but can be slow and memory-intensive because it searches blindly in all directions.

### 2. Depth-First Search (DFS)
* **Concept:** Dives as deep as possible along a single path until it hits a dead end, then backtracks.
* **Data Structure:** Stack (LIFO).
* **Characteristics:** Highly memory efficient, but it does **not** guarantee the shortest path. It mostly takes deeply winding routes.

### 3. Uniform Cost Search (UCS)
* **Concept:** Always expands the node with the lowest accumulated path cost $g(n)$ from the start.
* **Data Structure:** Priority Queue.
* **Characteristics:** Optimal for weighted graphs. However, in this unweighted maze (where every step costs exactly 1), it behaves identically to BFS.

### 4. Greedy Best-First Search (GBFS)
* **Concept:** A heuristic-driven search. It only looks at the estimated distance to the goal $h(n)$ (Manhattan distance) and runs directly toward it.
* **Data Structure:** Priority Queue (ordered by lowest $h(n)$).
* **Characteristics:** Very fast but **not** optimal. It easily gets trapped by obstacles and might trace an inefficient path.

### 5. A* Search (A-Star)
* **Concept:** The "smart" search. It combines the actual cost $g(n)$ (like UCS) and the estimated cost to the goal $h(n)$ (like Greedy).
* **Formula:** $f(n) = g(n) + h(n)$
* **Data Structure:** Priority Queue (ordered by lowest $f(n)$).
* **Characteristics:** The perfect balance. It guarantees the absolute shortest path while avoiding exploring unnecessary nodes, making it highly efficient. It is the industry standard for pathfinding in video games and robotics.

---

## 📂 Project Structure

- **Algorithm Modules:** `a_star.py`, `bfs.py`, `dfs.py`, `gbfs.py`, `ucs.py` - Contain the core logic for each respective algorithm.
- **Command-Line Interface:** `main.py` - Runs all algorithms on a simple maze and prints the computed paths to the terminal.
- **Visualizers (GUIs):** `gui_astar.py`, `gui_bfs.py`, `gui_dfs.py`, `gui_gbfs.py`, `gui_ucs.py` - Tkinter applications that provide a step-by-step visual animation of how each algorithm explores the maze grid.
- **Helpers:** `helper.py` - Contains shared utility functions.
- **Documentation:** `PRESENTATION.md` - A summary document outlining the performance and logic of the algorithms.

---

## 🚀 How to Run

### Command-Line Version
To quickly test all algorithms and see the path coordinate outputs, run `main.py`:

```bash
python main.py
```

### GUI Visualization
To visually observe how an algorithm searches the maze, run any of the `gui_` files. For example, to see the A* search in action:

```bash
python gui_astar.py
```
*(You can replace `gui_astar.py` with `gui_bfs.py`, `gui_dfs.py`, etc., to watch the other algorithms.)*

### Prerequisites
- Python 3.x
- `tkinter` (Usually comes pre-installed with standard Python distributions on Windows/macOS. Linux users may need to install it via their package manager, e.g., `sudo apt-get install python3-tk`).
