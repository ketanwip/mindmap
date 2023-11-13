# Double-click to create new node. 
# Double-click on node to create child node for it.

import tkinter as tk
from tkinter import simpledialog

class MindMapNode:
    def __init__(self, canvas, text, x, y):
        self.canvas = canvas
        self.text = text
        self.x = x
        self.y = y
        self.lines = []
        self.render()
        self.drag_data = {"x": 0, "y": 0, "item": None}

    def render(self):
        self.id = self.canvas.create_text(self.x, self.y, text=self.text, fill="black", font=('Arial', 16), tags="node")
        self.canvas.tag_bind(self.id, "<ButtonPress-1>", self.on_drag_start)
        self.canvas.tag_bind(self.id, "<ButtonRelease-1>", self.on_drag_stop)
        self.canvas.tag_bind(self.id, "<B1-Motion>", self.on_drag)
        #self.canvas.tag_bind(self.id, "<ButtonPress-3>", self.on_select)
        self.canvas.tag_bind(self.id, "<Double-Button-1>", self.on_select)

    def connect(self, node):
        # Calculate the offset for the start and end points of the line
        start_x, start_y = self.calculate_offset(self.x, self.y, node.x, node.y)
        end_x, end_y = node.calculate_offset(node.x, node.y, self.x, self.y)

        # Draw the line with the calculated offset
        line = self.canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST, fill="blue", width=2)
        self.lines.append(line)
        node.lines.append(line)

    def calculate_offset(self, x1, y1, x2, y2):
        bbox = self.canvas.bbox(self.id)
        if not bbox:
            return x1, y1

        # Calculate the center of the bounding box
        center_x = (bbox[0] + bbox[2]) / 2
        center_y = (bbox[1] + bbox[3]) / 2

        # Calculate the direction vector from the node to the target
        direction_x = x2 - center_x
        direction_y = y2 - center_y

        # Normalize the direction vector
        length = (direction_x**2 + direction_y**2)**0.5
        if length == 0:
            return x1, y1
        direction_x /= length
        direction_y /= length

        # Calculate the offset point
        offset_x = center_x + direction_x * (bbox[2] - bbox[0]) / 2
        offset_y = center_y + direction_y * (bbox[3] - bbox[1]) / 2

        return offset_x, offset_y


    def on_drag_start(self, event):
        self.drag_data["item"] = self.id
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_drag_stop(self, event):
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

    def on_drag(self, event):
        deltaX = event.x - self.drag_data["x"]
        deltaY = event.y - self.drag_data["y"]
        self.canvas.move(self.drag_data["item"], deltaX, deltaY)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.x, self.y = event.x, event.y
        self.update_lines()

    def update_lines(self):
        for line in self.lines:
            coords = self.canvas.coords(line)
            if coords[0] == self.x and coords[1] == self.y:
                self.canvas.coords(line, self.x, self.y, coords[2], coords[3])
            else:
                self.canvas.coords(line, coords[0], coords[1], self.x, self.y)

    def on_select(self, event):
        self.canvas.select_node = self
        # Optionally, highlight the selected node
        self.canvas.itemconfig(self.id, fill="red")  # Change color to indicate selection


class MindMapApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack(padx=10, pady=10)
        self.nodes = []
        self.canvas.bind("<Double-Button-1>", self.create_node)
        self.canvas.select_node = None

    def create_node(self, event):
        text = simpledialog.askstring("Input", "Enter node text", parent=self.root)
        if text:
            node = MindMapNode(self.canvas, text, event.x, event.y)
            if self.canvas.select_node:
                self.canvas.select_node.connect(node)
            self.nodes.append(node)
            self.canvas.select_node = None

root = tk.Tk()
app = MindMapApp(root)
root.title("Basic Mind Map App")
root.mainloop()
