import tkinter as tk
from tkinter import simpledialog

class MindMapNode:
    def __init__(self, canvas, text, x, y):
        self.canvas = canvas
        self.text = text
        self.x = x
        self.y = y
        self.render()
        self.drag_data = {"x": 0, "y": 0, "item": None}

    def render(self):
        self.id = self.canvas.create_text(self.x, self.y, text=self.text, fill="black", font=('Arial', 16), tags="node")
        self.canvas.tag_bind(self.id, "<ButtonPress-1>", self.on_drag_start)
        self.canvas.tag_bind(self.id, "<ButtonRelease-1>", self.on_drag_stop)
        self.canvas.tag_bind(self.id, "<B1-Motion>", self.on_drag)

    def connect(self, node):
        self.canvas.create_line(self.x, self.y, node.x, node.y, arrow=tk.LAST, fill="blue", width=2)

    def on_drag_start(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["item"] = item
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

class MindMapApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600, bg='yellow')
        self.canvas.pack(padx=10, pady=10)
        self.nodes = []
        self.canvas.bind("<Button-1>", self.create_node)

    def create_node(self, event):
        text = simpledialog.askstring("Input", "Enter node text", parent=self.root)
        if text:
            node = MindMapNode(self.canvas, text, event.x, event.y)
            if self.nodes:
                last_node = self.nodes[-1]
                last_node.connect(node)
            self.nodes.append(node)

root = tk.Tk()
app = MindMapApp(root)
root.title("Basic Mind Map App")
root.mainloop()
