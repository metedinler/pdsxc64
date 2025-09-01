import tkinter as tk

class GuiLibX:
    def __init__(self):
        self.root = tk.Tk()
        self.widgets = {}

    def create_window(self, title, width, height):
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")

    def add_button(self, name, text, x, y):
        button = tk.Button(self.root, text=text)
        button.place(x=x, y=y)
        self.widgets[name] = button

    def bind_event(self, widget_name, event_type, handler):
        widget = self.widgets.get(widget_name)
        if widget:
            widget.bind(event_type, handler)

    def run(self):
        self.root.mainloop()