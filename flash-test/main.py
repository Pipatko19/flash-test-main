import ttkbootstrap as ttk

from model import AppModel
from view import AppView
from controller import AppController

if __name__ == "__main__":
    root = ttk.Window(themename="simplex")
    root.title("Tester")
    root.geometry("1200x900")
    model = AppModel()
    view = AppView(root)
    controller = AppController(model, view)
    view.pack()
    root.mainloop()