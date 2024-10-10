import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk
from ttkbootstrap import constants as cn
from ttkbootstrap.scrolled import ScrolledText



class AppView(ttk.Frame):
    def __init__(self, root):
        """A program, that randomizes infrequent words
        with the purpose of testing your memory like flashcards."""

        
        super().__init__(root)

        self.icon = ImageTk.PhotoImage(file="./resources/settings_icon.png")
        self.icon_hovered = ImageTk.PhotoImage(file="./resources/settings_icon_hovered.png")


        style = ttk.Style()     
        style.configure(".", font=("garamond", 13))
        style.configure("Random.TButton", font=("garamond", 15), background="orange")
        style.configure("Invisible.TButton",  borderwidth=0, relief="flat", background="white")   

        style.map("Invisible.TButton", background=[("active", "white")], foreground=[("active", "green")])
        
        frm_display = ttk.Frame(self)
        frm_display.grid(column=0, row=0, columnspan=3, sticky="ew")        

        lfm_upper = ttk.LabelFrame(frm_display, text="title", style=cn.WARNING)
        lfm_upper.pack()

        lbl_upper_text = ttk.Label(lfm_upper, text= "Text Randomizer", font=("garamond", 30, "bold"), padding=10)
        lbl_upper_text.pack()

        self.txt_input_field: tk.Text = ScrolledText(frm_display, font="garamond 12", autohide=True)
        self.txt_input_field.pack(fill="both", expand=True, padx=20)

        # tags
        self.txt_input_field.tag_configure("Uncommon", background="#FF8C00")
        self.txt_input_field.tag_configure("Name", background="yellow")
        self.txt_input_field.tag_configure("Not_Found", background="red")
        self.txt_input_field.tag_configure("Short", background="#FAEBD7")
        self.txt_input_field.tag_configure("Normal", background="white")
        
        
        self.btn_randomizer = ttk.Button(self, text="Convert", width=20, style=("Random.TButton"))
        self.btn_randomizer.grid(column=1, row=1, ipadx=50, ipady=10, pady=20)
        
        self.btn_settings = ttk.Button(self, image=self.icon, style="Invisible.TButton")
        self.btn_settings.grid(column=2, row=1, sticky="n")
        
        self.btn_settings.bind("<Enter>", lambda event: self.btn_settings.config(image=self.icon_hovered))
        self.btn_settings.bind("<Leave>", lambda event: self.btn_settings.config(image=self.icon))
        
        self.columnconfigure([0, 1, 2], weight=1, minsize=100)
        
    def get_txt_input(self):
        return self.txt_input_field.get("1.0", tk.END)
    
    def update_tags(self, tag, start, end):
        self.txt_input_field.tag_add(tag, start, end)
    
if __name__ == "__main__":
    app = ttk.Window(themename='simplex')
    view = AppView(app)
    view.pack()
    app.mainloop()