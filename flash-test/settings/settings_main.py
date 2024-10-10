import tkinter as tk
import ttkbootstrap as ttk
from model import AppModel
from settings.blacklist import BlacklistUI

class Settings(ttk.Toplevel):
    def __init__(self, root, model:AppModel):
        super().__init__(root, resizable=(False, False))
        self.title("Settings")
        
        self.model = model
        
        frm_padding = ttk.Frame(self)

        frm_amplifier = ttk.Frame(frm_padding)

        lbl_scale_title = ttk.Label(frm_amplifier, text='rate of hidden words')
        lbl_scale_title.grid(column=0, row=0, columnspan=1)
        scl_bound = tk.Scale(frm_amplifier, from_=1, to=50, orient="horizontal", length=300, width=20, command=self.update_coeficient)
        scl_bound.grid(column=0, row=1)
        
        self.lbl_cur_coeficient = ttk.Label(frm_amplifier, text="1.5")
        self.lbl_cur_coeficient.grid(column=1, row=1, padx=8)
        
        self.black_list = BlacklistUI(self.model, frm_padding)
        
        frm_padding.pack(padx=20, pady=20)
        self.black_list.grid(column=1, row=0, rowspan=2, sticky="n", padx=10, pady=10)
        frm_amplifier.grid(column=0, row=0, sticky="n", padx=10, pady=10)
        
        self.protocol("WM_DELETE_WINDOW", self.quit)
        
    def update_coeficient(self, val):
        val = int(val) / 10
        self.model.bound_mute = val
        print(self.model.bound_mute)
        self.lbl_cur_coeficient.config(text=val)
    
    def quit(self):
        self.destroy()
        
if __name__ == "__main__":
    window = ttk.Window(themename="simplex")
    app = Settings(window, "")
    window.mainloop()