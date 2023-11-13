import tkinter as tk
from tkinter import simpledialog

class MindMapNode:
    def __init__(self, canvas, text, x, y):
        self.canvas = canvas
        self.text = text
        self.x = x
        self.y = y
        self.render()

    def render(self):
        self.id = self.canvas.create_text(self.x, self.y, text=self.text, fill="black", font=('Arial', 16), tags="node")


    def connect(self, node):
        self.canvas.create_line(self.x, self.y, node.x, node.y, arrow=tk.LAST, fill="blue", width=2)


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

