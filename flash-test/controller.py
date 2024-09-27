import re

from model import AppModel
from view import AppView

class AppController:
    def __init__(self, model: AppModel, view: AppView) -> None:
        self.model = model
        self.view = view
        self.view.btn_randomizer.config(command=self.convert)
        self.view.pack(expand=True, fill='both')
        
    def _format_lemmas(self, text) -> list[str]:
        """format the text before giving it to the lemanizator."""
        print("text:", text)
        concat_text = " ¶ ".join(text.splitlines()) #why does it have to be so stupid
        print("concat_text:", concat_text)
        lemmas = self.model.get_lemmatizator().get_lemmas(concat_text)
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
        text = self.view.get_txt_input()
        self.model.user_text = text
        word_indices = self._find_word_indices(text)
        lemmas = self._format_lemmas(text)

        for idx, word in enumerate(lemmas):
            if len(word) <= 3:
                tag = "Short"
            elif word and word[0].isupper():
                tag = "Name"
            elif word in self.model.get_word_data() or (not word.isalpha()):
                if word.isalpha() and self.model.get_word_data()[word] < 1000:
                    tag = "Uncommon"
                else:
                    tag = "Normal"
            else:
                tag = "Not_Found"
            self.view.update_tags(tag, *word_indices[idx])