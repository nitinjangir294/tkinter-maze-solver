import tkinter as tk
from queue import PriorityQueue, Queue
import time
import math

# Maze grid: 0 = path, 1 = wall
maze = [
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [1, 1, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0]
]

rows, cols = len(maze), len(maze[0])
start = (0, 0)
end = (4, 5)
cell_size = 60

root = tk.Tk()
root.title("Maze Solver - BFS / Dijkstra / A*")
canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size)
canvas.pack()

# ------------------- Drawing Functions -------------------
def draw_maze():
    for i in range(rows):
        for j in range(cols):
            color = "white" if maze[i][j] == 0 else "black"
            canvas.create_rectangle(
                j * cell_size, i * cell_size,
                (j + 1) * cell_size, (i + 1) * cell_size,
                fill=color, outline="gray"
            )

def mark_cell(i, j, color):
    canvas.create_rectangle(
        j * cell_size, i * cell_size,
        (j + 1) * cell_size, (i + 1) * cell_size,
        fill=color, outline="gray"
    )
    root.update()
    time.sleep(0.1)

def mark_path(parent):
    node = end
    while node:
        mark_cell(node[0], node[1], "green")
        node = parent[node]

# ------------------- Algorithms -------------------

def bfs():
    queue = Queue()
    queue.put(start)
    visited = set([start])
    parent = {start: None}

    while not queue.empty():
        x, y = queue.get()
        mark_cell(x, y, "lightblue")

        if (x, y) == end:
            mark_path(parent)
            return

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)
                queue.put((nx, ny))

    print("No path found!")

def dijkstra():
    pq = PriorityQueue()
    pq.put((0, start))
    distance = {start: 0}
    parent = {start: None}
    visited = set()

    while not pq.empty():
        dist, (x, y) = pq.get()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        mark_cell(x, y, "lightblue")

        if (x, y) == end:
            mark_path(parent)
            return

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                new_cost = dist + 1
                if (nx, ny) not in distance or new_cost < distance[(nx, ny)]:
                    distance[(nx, ny)] = new_cost
                    parent[(nx, ny)] = (x, y)
                    pq.put((new_cost, (nx, ny)))

    print("No path found!")

def heuristic(a, b):
    # Manhattan distance heuristic for A*
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar():
    pq = PriorityQueue()
    pq.put((0, start))
    g_cost = {start: 0}
    parent = {start: None}
    visited = set()

    while not pq.empty():
        _, (x, y) = pq.get()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        mark_cell(x, y, "lightblue")

        if (x, y) == end:
            mark_path(parent)
            return

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                new_g = g_cost[(x, y)] + 1
                f = new_g + heuristic((nx, ny), end)
                if (nx, ny) not in g_cost or new_g < g_cost[(nx, ny)]:
                    g_cost[(nx, ny)] = new_g
                    parent[(nx, ny)] = (x, y)
                    pq.put((f, (nx, ny)))

    print("No path found!")

# ------------------- Controls -------------------

def reset_maze():
    canvas.delete("all")
    draw_maze()

def start_bfs():
    reset_maze()
    root.after(500, bfs)

def start_dijkstra():
    reset_maze()
    root.after(500, dijkstra)

def start_astar():
    reset_maze()
    root.after(500, astar)

# ------------------- UI Buttons -------------------
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame, text="Solve using BFS", command=start_bfs, bg="#87CEFA").pack(side=tk.LEFT, padx=10)
tk.Button(frame, text="Solve using Dijkstra", command=start_dijkstra, bg="#FFD700").pack(side=tk.LEFT, padx=10)
tk.Button(frame, text="Solve using A*", command=start_astar, bg="#90EE90").pack(side=tk.LEFT, padx=10)

draw_maze()
root.mainloop()
