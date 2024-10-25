import ttkbootstrap as ttk

class NamedEntry(ttk.Entry):
    def __init__(self, word: str, width: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.word = word
        self.set_width = width + 2

        self.bind("<FocusOut>", self.unfocus)
        self.placeholder = self.word[0] + "-" * (len(self.word) - 1)
        
        self.bind("<Return>", self.unfocus)
        
    def insert_placeholder(self):
        self.delete(0, ttk.END)
        self.insert(0, self.placeholder)
        
    def _test(self):
        self.delete(0, ttk.END)
        self.insert(0, self.word)
        return self.word
        
    def get_width(self):
        return self.set_width
    
    def unfocus(self, event):
        cur_value = self.get().strip().lower()
        if cur_value == "skip":
            cur_value = self._test()
        if not cur_value or cur_value == self.placeholder:
            self.insert_placeholder()
            self.config(style="Primary.TEntry")
        elif cur_value == self.word:
            self.config(style="Correct.TEntry")
        else:
            self.config(style="Wrong.TEntry")
    
    def __str__(self) -> str:
        return "<{0}> - {1}".format(super().__str__(), self.word)