import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import constants as cn
from ttkbootstrap.scrolled import ScrolledText

class AppView(ttk.Frame):
    def __init__(self, root):
        """A program, that randomizes infrequent words
        with the purpose of testing your memory like flashcards."""

        
        super().__init__(root)

        style = ttk.Style()
        style.configure("TButton", font=("garamond", 15))

        lfm_upper = ttk.LabelFrame(self, text="title", style=cn.WARNING)
        lfm_upper.grid(column=0, row=0)
        lbl_upper_text = ttk.Label(lfm_upper, text= "Text Randomizer", font=("garamond", 30, "bold"), padding=10)
        lbl_upper_text.pack()

        self.txt_input_field: tk.Text = ScrolledText(self, font="garamond 12", autohide=True)
        self.txt_input_field.grid(column=0, row=1, sticky="ew", padx=20)

        #tags
        self.txt_input_field.tag_configure("Uncommon", background="#FF8C00")
        self.txt_input_field.tag_configure("Name", background="yellow")
        self.txt_input_field.tag_configure("Not_Found", background="red")
        self.txt_input_field.tag_configure("Short", background="#FAEBD7")
        self.txt_input_field.tag_configure("Normal", background="white")
        
        self.btn_randomizer = ttk.Button(self, text="Convert", width=20, style=("WARNING-TButton"))
        self.btn_randomizer.grid(column=0, row=2, ipadx=50, ipady=10, pady=20)
        
        self.columnconfigure([0], weight=1, minsize=500)
        
    def get_txt_input(self):
        return self.txt_input_field.get("1.0", tk.END)
    
    def update_tags(self, tag, start, end):
        self.txt_input_field.tag_add(tag, start, end)
    
if __name__ == '__main__':
    app = AppView()
    app.mainloop()