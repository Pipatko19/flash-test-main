import tkinter as tk
import ttkbootstrap as ttk

from PIL import ImageTk
from ttkbootstrap import constants as cn
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs.dialogs import Messagebox
import tkinter.font

from model import AppModel
from entry_name import NamedEntry

class AppView(ttk.Frame):
    def __init__(self, root, model: AppModel) -> None:
        """A program, that randomizes infrequent words
        with the purpose of testing your memory like flashcards."""

        
        super().__init__(root)
        self.model = model

        self.icon = ImageTk.PhotoImage(file="./resources/settings_icon.png")
        self.icon_hovered = ImageTk.PhotoImage(file="./resources/settings_icon_hovered.png")

        style = ttk.Style()     
        style.configure(".", font=("garamond", 13))
        style.configure("Random.TButton", font=("garamond", 15), background="orange")
        style.configure("Invisible.TButton",  borderwidth=0, relief="flat", background="white")
        style.map("Invisible.TButton", background=[("active", "white")], foreground=[("active", "green")])
        
        style.configure('TEntry', relief="flat", background="yellow", borderwidth=40)
        style.configure("Wrong.TEntry", fieldbackground="#ffb3b3")
        style.configure("Correct.TEntry", fieldbackground="#b3ffb3")
        
        
        self.frm_display = ttk.Frame(self)
        lfm_upper = ttk.LabelFrame(self.frm_display, text="MorphoDiTa's", style=cn.WARNING)

        lbl_upper_text = ttk.Label(lfm_upper, text= "Flash Randomizer", font=("garamond", 30, "bold"), padding=10)

        self.txt_input_field: tk.Text = ScrolledText(self.frm_display, font="garamond 12", autohide=True)
        self.default_font = tkinter.font.Font(family="garamond", size=12)
        
        self.frm_display.grid(column=0, row=0, columnspan=3, sticky="ew")        
        lfm_upper.pack()
        lbl_upper_text.pack()
        self.txt_input_field.pack(fill="both", expand=True, padx=20)
        
        self.btn_clear = ttk.Button(self, text="Clear", style=("Secondary.TButton"))
        self.btn_clear.grid(column=0, row=1, padx=10, ipadx=8, ipady=4)
        
        self.btn_randomizer = ttk.Button(self, text="Convert", width=20, style=("Random.TButton"))
        self.btn_randomizer.grid(column=1, row=1, ipadx=50, ipady=10, pady=10)
        
        self.btn_settings = ttk.Button(self, image=self.icon, style="Invisible.TButton")
        self.btn_settings.grid(column=2, row=1, pady=10)
        
        self.btn_settings.bind("<Enter>", lambda event: self.btn_settings.config(image=self.icon_hovered))
        self.btn_settings.bind("<Leave>", lambda event: self.btn_settings.config(image=self.icon))
        
        self.columnconfigure([0, 1, 2], weight=1, minsize=100)
        
        self.txt_input_field.bind_all('<MouseWheel>', self.on_mouse_wheel)  # For Windows and MacOS
        self.txt_input_field.bind_all('<Button-4>', self.on_mouse_wheel)    # For Linux (scroll up)
        self.txt_input_field.bind_all('<Button-5>', self.on_mouse_wheel)    # For Linux (scroll down)
        
    def create_winning_msg_box(self):
        """Display a congratulating messagebox"""
        Messagebox.ok("Congratulations, all is correct!")

    
    def get_txt_input(self):
        """return text from the text field"""
        return self.txt_input_field.get("1.0", tk.END)
    
    
    def create_entry(self, indices: list[str | float], tag) -> None:
        """replaces the word at the indices with an entry.
        Fuckin nefunguje protože word je lemma ne normální token aaaaaah

        Args:
            word (str): word
            indices (list[str  |  float]): starting and ending index
        """
        word = self.txt_input_field.get(*indices)
        width = self._calculate_width(word)

        entry = NamedEntry(word, width, len(self.model.entries), master=self.txt_input_field, font=('garamond', 9), style=tag)
        entry.insert_placeholder()
        self.model.entries.append((entry, indices[0]))

        
        bbox = self.txt_input_field.bbox(indices[0])
            
        if bbox is not None:
            start_x, y, width, height = bbox
            #end_x = self.txt_input_field.bbox(indices[1])[0]
            entry.place(x=start_x - 3, y=y, width=entry.get_width(), height=30)



        self.txt_input_field.update_idletasks()
    
    def on_mouse_wheel(self, event):
        """scrolls the text by a consistent ammount"""
        if event.delta:  # Windows and Mac 
            self.txt_input_field.text.yview_scroll(-1 * int(event.delta / 120), "units")
        else:  # Linux
            if event.num == 4:
                self.txt_input_field.text.yview_scroll(-1, "units")
            elif event.num == 5:
                self.txt_input_field.text.yview_scroll(1, "units")
        self.update_entry_positions()
    
    def update_entry_positions(self):
        """updates visible entries, places them on their word in the text"""
        for entry, index in self.model.entries:
            entry: NamedEntry
            bbox = self.txt_input_field.bbox(index)
            if bbox is not None:
                # Entry is visible, update position
                entry.place(x=bbox[0], y=bbox[1], width=entry.get_width(), height=30)
                entry.lift()  # Ensure the entry is on top of the text widget
            else:
                # Entry is out of view, hide it
                entry.place_forget()
    
    def _calculate_width(self, word):
        return self.default_font.measure(word)

    def disable_txt(self):
        self.txt_input_field.text.config(state=tk.DISABLED)
    
    def enable_txt(self):
        self.txt_input_field.text.config(state=tk.NORMAL)
    
    def clear_txt(self):
        print("Removed text")
        self.txt_input_field.delete("1.0", tk.END)

if __name__ == "__main__":
    app = ttk.Window(themename='simplex')
    view = AppView(app, "-")
    view.pack()
    app.mainloop()