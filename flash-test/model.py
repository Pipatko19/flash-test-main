from readers.morftest import Lemmatizator
from readers.frequency import Corpus
from entry_name import NamedEntry

class AppModel:
    def __init__(self, corpus_type="syn2015_lemma_utf8.tsv",lemmatizator_type="czech-morfflex2.0-pdtc1.0-220710-pos_only.tagger") -> None:
        self._word_data = Corpus("data/" + corpus_type).get_words()
        self._lemmatizator = Lemmatizator("data/" + lemmatizator_type)
        self.bound_mute: float = 1
        self._user_text: str = None
        self.hide_names: bool = None
        self.hide_unknowns: bool = None
        self.blacklist: set = AppModel.read_blacklist()
        self.entries: list[NamedEntry | str] = []
        
    @property
    def user_text(self):
        return self._user_text
    
    @user_text.setter
    def user_text(self, text: str) -> None:
        self._user_text = text
        print("recieved users text:", text)
    
    @property
    def lemmatizator(self):
        return self._lemmatizator
    @lemmatizator.setter
    def lemmatizator(self, _):
        raise ValueError("cannot overwrite lemmatizator")

    @property
    def word_data(self):
        return self._word_data
    @word_data.setter
    def word_data(self, _):
        raise ValueError("cannot overwrite corpus")
    
    @staticmethod
    def read_blacklist() -> set:
        data = set()
        with open("data/blacklisted_words.txt", "r") as f:
            for word in f:
                data.add(word.strip())
        return data
    
    def clear_entries(self):
        for entry, index in self.entries:
            entry.destroy()
        self.entries.clear()
    
    def save_blacklist(self) -> None:
        with open("data/blacklisted_words.txt", "w") as f:
            for word in self.blacklist:
                f.write(word + "\n")