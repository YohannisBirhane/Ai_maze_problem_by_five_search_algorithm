import tkinter as tk
from tkinter import ttk, messagebox
import time

# Import the algorithms
from a_star import astar
from bfs import bfs
from dfs import dfs
from gbfs import greedy
from ucs import ucs

class MazeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver Visualization - AI Algorithms")
        self.root.geometry("800x650")
        self.root.configure(bg="#2b2b2b")

        # Configuration
        self.cell_size = 40
        self.maze_data = [
            ["S", ".", ".", ".", ".", "#", ".", ".", ".", "."],
            ["#", "#", "#", ".", "#", "#", ".", "#", "#", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", "#", "#", "#", "#", "#", "#", "#", "#", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "G"],
            [".", "#", "#", "#", "#", "#", "#", "#", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        ]
        
        self.rows = len(self.maze_data)
        self.cols = len(self.maze_data[0])
        self.canvas_width = self.cols * self.cell_size
        self.canvas_height = self.rows * self.cell_size

        self.animation_speed = 0.8  # Much slower speed for very clear visibility
        self.is_running = False

        self.setup_ui()
        self.draw_maze()

    def setup_ui(self):
        # Top Control Frame
        control_frame = tk.Frame(self.root, bg="#3c3f41", pady=10)
        control_frame.pack(fill=tk.X)

        tk.Label(control_frame, text="Algorithm:", bg="#3c3f41", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)

        self.algo_var = tk.StringVar(value="BFS")
        algo_dropdown = ttk.Combobox(control_frame, textvariable=self.algo_var, state="readonly", width=10, font=("Arial", 12))
        algo_dropdown['values'] = ("BFS", "DFS", "UCS", "Greedy", "A*")
        algo_dropdown.pack(side=tk.LEFT, padx=5)

        run_btn = tk.Button(control_frame, text="▶ Run Search", bg="#4caf50", fg="white", font=("Arial", 12, "bold"), command=self.run_algorithm)
        run_btn.pack(side=tk.LEFT, padx=15)

        reset_btn = tk.Button(control_frame, text="🔄 Reset", bg="#f44336", fg="white", font=("Arial", 12, "bold"), command=self.reset_maze)
        reset_btn.pack(side=tk.LEFT, padx=5)

        clear_walls_btn = tk.Button(control_frame, text="Clear Walls", bg="#ff9800", fg="white", font=("Arial", 10), command=self.clear_walls)
        clear_walls_btn.pack(side=tk.LEFT, padx=20)

        tk.Label(control_frame, text="(Click grid to add/remove walls)", bg="#3c3f41", fg="#aaaaaa", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)

        # Canvas Frame
        canvas_frame = tk.Frame(self.root, bg="#2b2b2b")
        canvas_frame.pack(expand=True)

        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_width, height=self.canvas_height, bg="white", highlightthickness=2, highlightbackground="#555")
        self.canvas.pack(pady=20)
        
        # Bind mouse click for drawing walls
        self.canvas.bind("<B1-Motion>", self.toggle_wall)
        self.canvas.bind("<Button-1>", self.toggle_wall)

        # Status Label
        self.status_label = tk.Label(self.root, text="Ready. Select an algorithm and run.", bg="#2b2b2b", fg="#4fc3f7", font=("Arial", 14))
        self.status_label.pack(pady=5)

    def draw_maze(self):
        self.canvas.delete("all")
        self.rectangles = {}
        for r in range(self.rows):
            for c in range(self.cols):
                val = self.maze_data[r][c]
                color = self.get_color(val)
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#cccccc")
                self.rectangles[(r, c)] = rect
                
                # Add text for S and G
                if val in ['S', 'G']:
                    self.canvas.create_text(x1 + self.cell_size/2, y1 + self.cell_size/2, text=val, font=("Arial", 16, "bold"), fill="white")

    def get_color(self, val):
        if val == 'S': return "#4caf50" # Green
        if val == 'G': return "#f44336" # Red
        if val == '#': return "#333333" # Dark Gray (Wall)
        return "#ffffff" # White (Free)

    def reset_maze(self):
        if self.is_running: return
        self.status_label.config(text="Maze reset. Ready.", fg="#4fc3f7")
        self.draw_maze()

    def clear_walls(self):
        if self.is_running: return
        for r in range(self.rows):
            for c in range(self.cols):
                if self.maze_data[r][c] == '#':
                    self.maze_data[r][c] = '.'
        self.draw_maze()

    def toggle_wall(self, event):
        if self.is_running: return
        c = event.x // self.cell_size
        r = event.y // self.cell_size
        if 0 <= r < self.rows and 0 <= c < self.cols:
            if self.maze_data[r][c] not in ['S', 'G']:
                val = self.maze_data[r][c]
                new_val = '#' if val == '.' else '.'
                self.maze_data[r][c] = new_val
                
                # Update just this rectangle
                color = self.get_color(new_val)
                self.canvas.itemconfig(self.rectangles[(r, c)], fill=color)

    def run_algorithm(self):
        if self.is_running: return
        self.reset_maze()
        self.is_running = True
        algo_name = self.algo_var.get()
        self.status_label.config(text=f"Running {algo_name}...", fg="#ffeb3b")

        algorithms = {
            "BFS": bfs,
            "DFS": dfs,
            "UCS": ucs,
            "Greedy": greedy,
            "A*": astar
        }
        
        func = algorithms[algo_name]
        try:
            # We now expect algorithms to return (path, visited_order)
            result = func(self.maze_data)
            if isinstance(result, tuple) and len(result) == 2:
                path, visited_order = result
            else:
                path = result
                visited_order = [] # Fallback if algorithm not modified
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", fg="#f44336")
            self.is_running = False
            return

        self.animate(path, visited_order, algo_name)

    def animate(self, path, visited_order, algo_name):
        # Animate Exploration
        def show_visited(index):
            if index < len(visited_order):
                r, c = visited_order[index]
                if self.maze_data[r][c] not in ['S', 'G']:
                    self.canvas.itemconfig(self.rectangles[(r, c)], fill="#81d4fa") # Light Blue
                self.root.after(int(self.animation_speed * 1000), show_visited, index + 1)
            else:
                # After visiting, show path
                if path:
                    self.status_label.config(text=f"{algo_name}: Path Found! (Length: {len(path)-1})", fg="#4caf50")
                    show_path(0)
                else:
                    self.status_label.config(text=f"{algo_name}: No path exists!", fg="#f44336")
                    self.is_running = False

        # Animate Final Path
        def show_path(index):
            if index < len(path):
                r, c = path[index]
                if self.maze_data[r][c] not in ['S', 'G']:
                    self.canvas.itemconfig(self.rectangles[(r, c)], fill="#ffeb3b") # Yellow
                self.root.after(int(self.animation_speed * 1000), show_path, index + 1)
            else:
                self.is_running = False

        if visited_order:
            show_visited(0)
        elif path:
            show_path(0)
        else:
            self.status_label.config(text=f"{algo_name}: No path exists!", fg="#f44336")
            self.is_running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeGUI(root)
    root.mainloop()
