import tkinter as tk
import ttkbootstrap as ttk
from model import AppModel
from settings.blacklist import BlacklistUI
from settings.toggleables import Toggleables

class Settings(ttk.Toplevel):
    """Change how the program determines uncommon words."""
    def __init__(self, root, model:AppModel) -> None:
        super().__init__(root, resizable=(False, False))
        self.title("Settings")
        
        self.model = model
        
        frm_padding = ttk.Frame(self)
        frm_padding.pack(padx=20, pady=20)

        frm_amplifier = ttk.Frame(frm_padding)
        
        lbl_scale_title = ttk.Label(frm_amplifier, text='rate of hidden words')
        scl_bound = tk.Scale(frm_amplifier, from_=1, to=50, orient="horizontal", length=300, width=20, command=self.update_coeficient)
        self.lbl_cur_coeficient = ttk.Label(frm_amplifier, text="1")
        
        frm_amplifier.grid(column=0, row=0, sticky="n", padx=10, pady=10)
        lbl_scale_title.grid(column=0, row=0, columnspan=1)
        scl_bound.grid(column=0, row=1)
        self.lbl_cur_coeficient.grid(column=1, row=1, padx=8)
        
        self.hidings = Toggleables(self.model, frm_padding)
        self.hidings.grid(column=0, row=1, sticky="n")

        
        self.black_list = BlacklistUI(self.model, frm_padding)
        self.black_list.grid(column=1, row=0, rowspan=2, sticky="n", padx=10, pady=10)
        
        btn_save = ttk.Button(frm_padding, text="Save", command=model.save_blacklist, style="secondary.tButton")
        btn_save.grid(column=1, row=2)

        
        
    def update_coeficient(self, val: str):
        """Displays the current mute to the user"""
        val = int(val) / 10
        self.model.bound_mute = val
        print(self.model.bound_mute)
        self.lbl_cur_coeficient.config(text=val)

        
if __name__ == "__main__":
    window = ttk.Window(themename="simplex")
    app = Settings(window, "")
    window.mainloop()