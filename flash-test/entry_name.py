import ttkbootstrap as ttk

class NamedEntry(ttk.Entry):
    def __init__(self, word: str, width: int, idx, *args, **kwargs):
        #Entry with an assigned word.
        super().__init__(*args, **kwargs)
        self.word = word
        self.set_width = width + 4
        self.idx = idx
        self.state = False

        self.placeholder = self.word[0] + "*" * (len(self.word) - 1)
    
        self.bind("<FocusOut>", self.unfocus)
        self.bind("<Return>", self.unfocus)
        
    def insert_placeholder(self):
        #Writes the hidden word.
        self.delete(0, ttk.END)
        self.insert(0, self.placeholder)
        
    def correct_update(self):
        #Writes the whole word.
        self.delete(0, ttk.END)
        self.insert(0, self.word)
        
    def get_width(self):
        return self.set_width
    
    def unfocus(self, event):
        #Checks the state of the entry when the user stops focusing.
        cur_value = self.get().strip().lower()
        self.state = False
        if cur_value == "skip":
            cur_value = self.word.lower()
        if not cur_value or cur_value == self.placeholder.lower(): #empty
            self.insert_placeholder()
            self.config(style="Primary.TEntry")

        elif cur_value == self.word.lower():
            self.config(style="Correct.TEntry")
            self.state = True
            self.correct_update()
        else:
            self.config(style="Wrong.TEntry")            
            
    
    def __str__(self) -> str:
        return "<{0}> - {1}".format(super().__str__(), self.word)