import tkinter as tk
import ttkbootstrap as ttk

class Settings(ttk.Toplevel):
    def __init__(self, root, model):
        super().__init__(root)
        self.title("Settings")
        self.geometry("450x200")
        
        self.model = model
        

        frm_amplifier = ttk.Frame(self)
        frm_amplifier.pack()
        
        lbl_scale_title = ttk.Label(frm_amplifier, text='amplify quantity of hidden words')
        lbl_scale_title.grid(column=0, row=0, columnspan=1)
        
        scl_bound = tk.Scale(frm_amplifier, from_=0, to=200, orient="horizontal", length=200, width=20, command=self.update_coeficient)
        scl_bound.grid(column=0, row=1, padx=20)
        
        self.lbl_cur_coeficient = ttk.Label(frm_amplifier, text="1.5")
        self.lbl_cur_coeficient.grid(column=1, row=1, padx=8)
        
    def update_coeficient(self, val):
        print(val)
        self.lbl_cur_coeficient.config(text=val)
        
if __name__ == "__main__":
    window = ttk.Window(themename="simplex")
    app = Settings(window, "")
    window.mainloop()