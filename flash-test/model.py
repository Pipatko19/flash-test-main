from readers.morftest import Lemmatizator
from readers.frequency import Corpus


class AppModel:
    def __init__(self, corpus_type="syn2015_lemma_utf8.tsv",lemmatizator_type="czech-morfflex2.0-pdtc1.0-220710-pos_only.tagger") -> None:
        self._word_data = Corpus("data/" + corpus_type).get_words()
        self._lemmatizator = Lemmatizator("data/" + lemmatizator_type)
        self.bound_mute: float = 1
        self.score_bound: float = None
        self._user_text: str = None
        self.blacklist: set = AppModel.read_blacklist()
        

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
    
    def save_blacklist(self) -> None:
        with open("data/blacklisted_words.txt", "w") as f:
            for word in self.blacklist:
                f.write(word + "\n")