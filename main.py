import re

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import constants as cn
from ttkbootstrap.scrolled import ScrolledText

from morftest import lemmatizator
from frequency import corpus

class App(ttk.Window):
    def __init__(self):
        """A program, that randomizes infrequent words
        with the purpose of testing your memory like flashcards."""
        self.word_data = corpus.get_words()
        self.lemm = lemmatizator
        
        super().__init__(themename="simplex")
        self.title("Tester")
        self.geometry("1200x900")

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
        
        btn_randomizer = ttk.Button(self, text="Convert", width=20, style=("WARNING-TButton"), command=self.convert)
        btn_randomizer.grid(column=0, row=2, ipadx=50, ipady=10, pady=20)
        self.columnconfigure([0], weight=1, minsize=500)

    def _format_lemmas(self, text) -> list[str]:
        """format the text before giving it to the lemanizator."""
        print("text:", text)
        concat_text = " ¶ ".join(text.splitlines()) #why does it have to be so stupid
        print("concat_text:", concat_text)
        lemmas = self.lemm.get_lemmas(concat_text)
        print("lemmas:", lemmas)
        return lemmas
    
    def _find_word_indices(self, test_str) -> list[str | float]:
        """finds the starting and ending indices of each word."""
        word_indices = []
        start_index = [1, 0]
        between_symbols = {"-", "/", "="}
        past_char_count = 0
        for i in range(len(test_str)):
        
            if re.match(r'^[^\w]+$', test_str[i]):
                if not (test_str[i] in between_symbols and
                    (i != 0 and test_str[i - 1].isalpha()) and
                    (i != len(test_str) and test_str[i + 1].isalpha())):
                    if start_index[1] != i:
                        proc_start = list(start_index)
                        proc_start[1] -= past_char_count
                        word_indices.append((".".join(map(str, proc_start)), str(start_index[0]) + "." + str(i - past_char_count)))
                if test_str[i] == "\n":
                    start_index[0] += 1
                    past_char_count = i + 1
                start_index[1] = i + 1
                
        if start_index[1] != len(test_str):
            proc_start = list(start_index)
            proc_start[1] -= past_char_count
            word_indices.append((".".join(map(str, proc_start)), str(start_index[0]) + "." + str(len(test_str) - past_char_count)))
        return word_indices


    def convert(self):
        """Hides the least common words in the text field."""
        text = self.txt_input_field.get("1.0", tk.END)
        word_indices = self._find_word_indices(text)
        lemmas = self._format_lemmas(text)

        for idx, word in enumerate(lemmas):
            if len(word) <= 3:
                tag = "Short"
            elif word and word[0].isupper():
                tag = "Name"
            elif word in self.word_data or (not word.isalpha()):
                if word.isalpha() and self.word_data[word] < 1000:
                    tag = "Uncommon"
                else:
                    tag = "Normal"
            else:
                tag = "Not_Found"
            self.txt_input_field.tag_add(tag, *word_indices[idx])
if __name__ == "__main__":
    ran = App()
    ran.mainloop()