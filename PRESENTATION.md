# AI Pathfinding in a Maze: Algorithm Presentation

## 1. Introduction & Problem Statement
**The Problem:** Given a 2D grid maze, an AI agent must find a path from the **Start (S)** to the **Goal (G)** without passing through walls/obstacles (**#**). 
**Objective:** Compare different Artificial Intelligence search algorithms to find the shortest path efficiently. Each step to an adjacent cell costs exactly `1`.

---

## 2. Algorithms Overview

### 🟢 1. Breadth-First Search (BFS)
* **Concept:** Explores equally in all directions, expanding layer by layer (like a water ripple).
* **Data Structure:** Queue (FIFO - First In, First Out).
* **GUI Metric:** Depth (Level from the start).
* **Pros:** *Optimal & Complete.* It guarantees the shortest path no matter what.
* **Cons:** *Blind Search.* Because it looks in all directions uniformly, it explores many unnecessary cells, taking more time and memory.

### 🟠 2. Depth-First Search (DFS)
* **Concept:** Dives as deep as possible along a single path until it hits a dead end, then backtracks to try another path.
* **Data Structure:** Stack (LIFO - Last In, First Out).
* **GUI Metric:** Depth (Level from the start).
* **Pros:** *Memory Efficient.* Uses less memory than BFS. Can sometimes find the goal quickly if it chooses the right path by luck.
* **Cons:** *Not Optimal.* It almost never finds the shortest path, often taking long, winding routes. 

### 🟣 3. Uniform Cost Search (UCS)
* **Concept:** Always expands the node with the lowest accumulated path cost $g(n)$ from the start. "How much did it cost me to get here?"
* **Data Structure:** Priority Queue (Ordered by lowest $g(n)$).
* **GUI Metric:** Actual Cost $g(n)$.
* **Pros:** *Optimal.* Guarantees the shortest path, especially useful in graphs where different paths have different costs (hills, swamps).
* **Cons:** In this unweighted maze (where every step costs exactly 1), UCS behaves identically to BFS and wastes time looking in the wrong directions.

### 🔴 4. Greedy Best-First Search (GBFS)
* **Concept:** A heuristic (guess) driven search. "Greedy" because it only looks at the estimated distance to the goal $h(n)$ and completely forgets how far it has traveled.
* **Heuristic Used:** Manhattan Distance to the Goal.
* **Data Structure:** Priority Queue (Ordered by lowest $h(n)$).
* **GUI Metric:** Computed Heuristic $h(n)$.
* **Pros:** *Very Fast.* Runs directly toward the goal, skipping many nodes.
* **Cons:** *Not Optimal.* Easily gets trapped by obstacles (walls) and will often trace an inefficient path just because it "looks" closer to the goal initially.

### 🌟 5. A* Search (A-Star) - The Best of Both Worlds
* **Concept:** The "smart" search. It combines the actual cost traveled $g(n)$ from UCS and the estimated cost to the goal $h(n)$ from Greedy.
* **Formula:** $f(n) = g(n) + h(n)$
    * $g(n)$ = Cost from Start to current node.
    * $h(n)$ = Estimated cost from current node to Goal.
    * $f(n)$ = Total estimated cost of the path.
* **Data Structure:** Priority Queue (Ordered by lowest $f(n)$).
* **GUI Metric:** $f(n), g(n), \text{and } h(n)$.
* **Pros:** *Optimal & Efficient.* It guarantees the shortest path (like BFS/UCS) but explores far fewer nodes by moving intelligently toward the goal (like Greedy).
* **Cons:** Takes slightly more CPU power per node to calculate the heuristic, but saves massive amounts of time overall.

---

## 3. Conclusion & Summary
When developing an AI for Pathfinding (like in our Maze or Video Games):
* Use **BFS / UCS** when you want the shortest path but don't know the location of the goal (No Heuristic).
* Use **DFS** when memory is highly constrained and path length doesn't matter.
* Use **Greedy Best-First** when you need blazing fast speed but don't strictly need the absolute shortest path.
* Use **A* Search** as the industry standard. It is the perfect balance, guaranteeing the optimal path while maintaining high performance.
