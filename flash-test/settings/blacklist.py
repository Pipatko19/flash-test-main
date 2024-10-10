import ttkbootstrap as ttk
import tkinter as tk

from model import AppModel

class BlacklistUI(ttk.Frame):
    def __init__(self, model:AppModel, master, *args, **kwargs):
        self.model = model
        super().__init__(master, *args, **kwargs)
        lbl_change = ttk.Label(self, text="Blacklist")
        lbl_change.pack()
        
        frm_change = ttk.Frame(self)
        self.ent_word = ttk.Entry(frm_change)
        self.ent_word.grid(column=0, row=0, columnspan=2, pady=5)
        
        btn_add = ttk.Button(frm_change, text="Add", command=self.add_word, style="SUCCESS.TButton")
        btn_add.grid(column=0, row=1)
        
        btn_remove = ttk.Button(frm_change, text="Remove", command=self.remove_word, style="WARNING.TButton")
        btn_remove.grid(column=1, row=1)
        
        frm_change.pack()
        
        lbl_name = ttk.Label(self, text="Blacklisted Words")
        lbl_name.pack()
        
        scrollbar = ttk.Scrollbar(self)
        self.lstbox_blaclisted = ttk.Treeview(self, selectmode="browse", yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.lstbox_blaclisted.yview)
        scrollbar.pack()
        self.lstbox_blaclisted.pack()
        
    def add_word(self):
        word = self.ent_word.get().strip()
        
        self.model.blacklist.add(word)
        self.lstbox_blaclisted.insert("", tk.END, iid=word, text=word)
        self.ent_word.delete(0, tk.END)  # Clear the entry

    def remove_word(self):
        word = self.lstbox_blaclisted.selection()[0]
        self.model.blacklist.remove(word)
        self.lstbox_blaclisted.delete(word)

if __name__ == "__main__":
    window = ttk.Window(themename="simplex")
    blacklist = BlacklistUI(window)
    blacklist.grid(row=0, column=0)
    window.mainloop()