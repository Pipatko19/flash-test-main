import re
import numpy as np

from model import AppModel
from view import AppView
from settings.settings_main import Settings
from entry_name import NamedEntry
from tkinter import BooleanVar

class AppController:
    def __init__(self, model: AppModel, view: AppView) -> None:
        self.model = model
        self.view = view
        self.view.btn_clear.config(command=self.reset_all)
        self.view.btn_randomizer.config(command=self.convert)
        self.view.btn_settings.config(command=self.open_settings)
        self.view.pack(expand=True, fill='both')
        self.view.bind_all("<Return>", self.focus_next_entry)
        self.view.bind_all("<Shift-Left>", self.focus_prev_entry)
        self.view.bind_all("<Shift-Right>", self.focus_next_entry)
        self.model.hide_names = BooleanVar(value=False)
        self.model.hide_unknowns = BooleanVar(value=False)
        
    def check_all_done(self, event):
        if event.widget.state:
            for entry, idx in self.model.entries:
                if not entry.state:
                    return
            self.view.create_winning_msg_box()
            
    def focus_next_entry(self, event):
        widget: NamedEntry = event.widget
        print("Registered widget:", widget.winfo_name())
        if isinstance(widget, NamedEntry):
            self.check_all_done(event)
            if widget.idx < len(self.model.entries) - 1:
                self.model.entries[widget.idx + 1][0].focus()
                
    def focus_prev_entry(self, event):
        widget: NamedEntry = event.widget
        print("Registered widget:", widget.winfo_name())
        if isinstance(widget, NamedEntry):
            if widget.idx > 0:
                self.model.entries[widget.idx - 1][0].focus()
        
    def lower_bound(self, text: list) -> float:
        """calculate the lower bound on a logarithmic scale"""
        data = self.model.word_data
        frequencies = []
        for word in text:
            if word in data:
                frequencies.append(data[word])
        frequencies = np.log10(frequencies)
        #print(frequencies)
        log_mean = np.mean(frequencies)
        log_std = np.std(frequencies) * self.model.bound_mute
        print("mean:", log_mean)
        print("std:", log_std)
        return log_mean - log_std
                
        
    def _format_lemmas(self, text: str) -> list[str]:
        """formats the text before giving it to the lemanizator."""
        #print("text:", text)
        concat_text = " ¶ ".join(text.splitlines()) #why does it have to be so stupid
        #print("concat_text:", concat_text)
        lemmas = self.model.lemmatizator.get_lemmas(concat_text)
        print("\nlemmas:", lemmas)
        return lemmas
    
    def _find_word_indices(self, text) -> list[str | float]:
        """finds the starting and ending index of each word (in "y.x" format)"""
        word_indexes = []
        pattern = re.compile(r'\b[\w./,-]+(?:[\w./,-]+)*\b')  # Pattern for words with hyphens and decimal points
        y = 1
        prev = -1
        i = 0  
        while i < len(text):
            if text[i] == '\n':
                y += 1 
                prev = i
                i += 1
            else:
                # Check for word using the regex pattern from the current position
                match = pattern.match(text[i:])
                if match:
                    start_index = i - prev - 1
                    word_length = len(match.group())
                    end_index = start_index + word_length
                    word_indexes.append((str(y) + "." + str(start_index), str(y) + "." + str(end_index)))
                    i += word_length 
                else:
                    i += 1  # Move forward if no match
        print("\nINDEXES:", *(self.view.txt_input_field.get(start,end) for start, end in word_indexes), sep=", ")
        return word_indexes

    def _reset(self) -> None:
        self.model.clear_entries()
        self.view.enable_txt()
    
    def reset_all(self) -> None:
        self._reset()
        self.view.clear_txt()
    
    def convert(self) -> None:
        """Hides the least common words in the text field."""
        self._reset()
        self.view.disable_txt()
        
        text = self.view.get_txt_input()
        self.model.user_text = text
        word_indices = self._find_word_indices(text)
        lemmas = self._format_lemmas(text)
        lower_bound = self.lower_bound(lemmas)
        for idx, word in enumerate(lemmas):
            if word not in self.model.blacklist and word.isalpha() and len(word) > 3:
                if word[0].isupper():
                    if self.model.hide_names.get():
                        self.view.create_entry(word_indices[idx], tag="WARNING.TEntry")
                    continue
                    
                if word not in self.model.word_data:
                    if self.model.hide_unknowns.get():
                        self.view.create_entry(word_indices[idx], tag="DANGER.TEntry")
                    continue
                elif np.log10(self.model.word_data[word]) < lower_bound:
                    self.view.create_entry(word_indices[idx], tag="PRIMARY.TEntry")

                    
    def open_settings(self):
        """Creates settings window."""
        if not hasattr(self, "settings_window") or not self.settings_window.winfo_exists():
            self.settings_window = Settings(self.view, self.model)
            self.settings_window.attributes("-topmost", "true")