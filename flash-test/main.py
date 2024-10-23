import ttkbootstrap as ttk

from model import AppModel
from view import AppView
from controller import AppController

if __name__ == "__main__":
    model = AppModel()
    root = ttk.Window(themename="simplex")
    root.title("Tester")
    root.geometry("1200x900")
    view = AppView(root, model)
    controller = AppController(model, view)
    view.pack()
    root.mainloop()