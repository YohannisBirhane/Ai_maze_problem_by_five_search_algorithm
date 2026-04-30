import tkinter as tk
from tkinter import ttk, messagebox
import time

from gbfs import greedy

class GBFSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver - Greedy Best-First Search")
        self.root.geometry("800x650")
        self.root.configure(bg="#2b2b2b")

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
        control_frame = tk.Frame(self.root, bg="#3c3f41", pady=10)
        control_frame.pack(fill=tk.X)

        tk.Label(control_frame, text="Algorithm: Greedy", bg="#3c3f41", fg="#ef5350", font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=20)

        run_btn = tk.Button(control_frame, text="▶ Run Greedy", bg="#4caf50", fg="white", font=("Arial", 12, "bold"), command=self.run_algorithm)
        run_btn.pack(side=tk.LEFT, padx=15)

        reset_btn = tk.Button(control_frame, text="🔄 Reset", bg="#f44336", fg="white", font=("Arial", 12, "bold"), command=self.reset_maze)
        reset_btn.pack(side=tk.LEFT, padx=5)

        clear_walls_btn = tk.Button(control_frame, text="Clear Walls", bg="#ff9800", fg="white", font=("Arial", 10), command=self.clear_walls)
        clear_walls_btn.pack(side=tk.LEFT, padx=20)

        canvas_frame = tk.Frame(self.root, bg="#2b2b2b")
        canvas_frame.pack(expand=True)

        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_width, height=self.canvas_height, bg="white", highlightthickness=2, highlightbackground="#555")
        self.canvas.pack(pady=20)
        
        self.canvas.bind("<B1-Motion>", self.toggle_wall)
        self.canvas.bind("<Button-1>", self.toggle_wall)

        self.status_label = tk.Label(self.root, text="Ready. Click 'Run GBFS' to start.", bg="#2b2b2b", fg="#4fc3f7", font=("Arial", 14))
        self.status_label.pack(pady=5)
        
        self.cost_label = tk.Label(self.root, text="Current Cost: 0", bg="#2b2b2b", fg="#ffeb3b", font=("Arial", 14, "bold"))
        self.cost_label.pack(pady=2)

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
                
                if val in ['S', 'G']:
                    self.canvas.create_text(x1 + self.cell_size/2, y1 + self.cell_size/2, text=val, font=("Arial", 16, "bold"), fill="white")

    def get_color(self, val):
        if val == 'S': return "#4caf50"
        if val == 'G': return "#f44336"
        if val == '#': return "#333333"
        return "#ffffff"

    def reset_maze(self):
        if self.is_running: return
        self.status_label.config(text="Maze reset. Ready.", fg="#4fc3f7")
        self.cost_label.config(text="Current Cost: 0")
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
                
                color = self.get_color(new_val)
                self.canvas.itemconfig(self.rectangles[(r, c)], fill=color)

    def run_algorithm(self):
        if self.is_running: return
        self.reset_maze()
        self.is_running = True
        self.status_label.config(text="Running Greedy Best-First...", fg="#ffeb3b")

        try:
            result = greedy(self.maze_data)
            if isinstance(result, tuple) and len(result) == 3:
                path, visited_order, costs_info = result
            elif isinstance(result, tuple) and len(result) == 2:
                path, visited_order = result
                costs_info = {}
            else:
                path = result
                visited_order = []
                costs_info = {}
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", fg="#f44336")
            self.is_running = False
            return

        self.animate(path, visited_order, costs_info, "Greedy Best-First")

    def animate(self, path, visited_order, costs_info, algo_name):
        self.cost_label.config(text="Exploring nodes...")

        def show_visited(index):
            if index < len(visited_order):
                r, c = visited_order[index]
                if self.maze_data[r][c] not in ['S', 'G']:
                    self.canvas.itemconfig(self.rectangles[(r, c)], fill="#ef9a9a") # Pinkish red
                    
                    if (r, c) in costs_info:
                        info = costs_info[(r, c)]
                        x1, y1 = c * self.cell_size, r * self.cell_size
                        text = f"h:{info['h']}"
                        self.canvas.create_text(x1 + self.cell_size/2, y1 + self.cell_size/2, text=text, font=("Arial", 10, "bold"), fill="#333")
                        self.cost_label.config(text=f"Visiting ({r},{c}) | h(n)={info['h']} (Heuristic)")

                self.root.after(int(self.animation_speed * 1000), show_visited, index + 1)
            else:
                if path:
                    self.status_label.config(text=f"{algo_name}: Path Found! (Length: {len(path)-1})", fg="#4caf50")
                    show_path(0)
                else:
                    self.status_label.config(text=f"{algo_name}: No path exists!", fg="#f44336")
                    self.cost_label.config(text="Current Cost: N/A")
                    self.is_running = False

        def show_path(index):
            if index < len(path):
                r, c = path[index]
                self.cost_label.config(text=f"Final Path Step: {index}")
                if self.maze_data[r][c] not in ['S', 'G']:
                    self.canvas.itemconfig(self.rectangles[(r, c)], fill="#ffeb3b")
                    
                    x1, y1 = c * self.cell_size, r * self.cell_size
                    self.canvas.create_text(x1 + self.cell_size/2, y1 + self.cell_size/2, text=str(index), font=("Arial", 12, "bold"), fill="black")

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
    app = GBFSGUI(root)
    root.mainloop()