import ttkbootstrap as ttk
from model import AppModel

class Toggleables(ttk.Frame):
    def __init__(self, model: AppModel, master=None, **args):
        super().__init__(master, **args)
        
        chk_names = ttk.Checkbutton(self, text="Hide Names", variable=model.hide_names, style="round.toggle")
        chk_names.pack()
        
        chk_unknows = ttk.Checkbutton(self, text="Hide Unknown Words", variable=model.hide_unknowns, style="round.toggle")
        chk_unknows.pack()


if __name__ == "__main__":
    app = ttk.Window()
    toggs = Toggleables(app, "-")
    app.mainloop()