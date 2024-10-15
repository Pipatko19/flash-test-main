import ttkbootstrap as ttk
import tkinter as tk

from model import AppModel

class BlacklistUI(ttk.Frame):
    def __init__(self, model:AppModel, master=None, *args, **kwargs) -> None:
        self.model = model
        super().__init__(master, *args, **kwargs)
        lbl_change = ttk.Label(self, text="Blacklist")
        lbl_change.pack()
        
        frm_change = ttk.Frame(self)
        
        self.ent_word = ttk.Entry(frm_change)
        btn_add = ttk.Button(frm_change, text="Add", command=self.add_word, style="SUCCESS.TButton")
        btn_remove = ttk.Button(frm_change, text="Remove", command=self.remove_word, style="WARNING.TButton")
        
        
        frm_change.pack()
        self.ent_word.grid(column=0, row=0, columnspan=2, pady=5)
        btn_add.grid(column=0, row=1)
        btn_remove.grid(column=1, row=1)

        lbl_name = ttk.Label(self, text="Blacklisted Words")
        lbl_name.pack()
        
        frm_view = ttk.Frame(self)
        
        scrollbar = ttk.Scrollbar(frm_view)
        self.lstbox_blacklist = ttk.Treeview(frm_view, selectmode="browse", yscrollcommand=scrollbar.set, show='tree')
        scrollbar.configure(command=self.lstbox_blacklist.yview)
        self._load_words()
        
        frm_view.pack()
        self.lstbox_blacklist.pack(side="left", fill="y")
        scrollbar.pack(side="right", fill="both")


        
    def _load_words(self) -> None:
        """Loads blacklisted words from the model."""
        for word in self.model.blacklist:
            self.lstbox_blacklist.insert("", tk.END, iid=word, text=word)
        
    def add_word(self) -> None:
        """adds the word to the blacklist"""
        word = self.ent_word.get().strip()
        word = self.model.lemmatizator.get_lemmas(word)[0]
        print(word)
        
        self.model.blacklist.add(word)
        self.lstbox_blacklist.insert("", tk.END, iid=word, text=word)
        self.ent_word.delete(0, tk.END)  # Clear the entry

    def remove_word(self) -> None:
        """removes the word from the blacklist"""
        word = self.lstbox_blacklist.selection()[0]
        self.model.blacklist.remove(word)
        self.lstbox_blacklist.delete(word)

if __name__ == "__main__":
    window = ttk.Window(themename="simplex")
    blacklist = BlacklistUI(window)
    blacklist.grid(row=0, column=0)
    window.mainloop()