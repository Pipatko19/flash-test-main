from readers.morftest import lemmatizator
from readers.frequency import corpus


class AppModel:
    def __init__(self):
        self.word_data = corpus.get_words()
        self.lemm = lemmatizator
        self._user_text: str = None
        
    @property
    def user_text(self):
        return self._user_text
    
    @user_text.setter
    def user_text(self, text: str) -> None:
        self._user_text = text
        print("recieved users text:", text)
    
    def get_lemmatizator(self):
        return self.lemm

    def get_word_data(self):
        return self.word_data
