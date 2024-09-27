import ufal.morphodita
import nltk
import re
nltk.download('punkt_tab')

class Lemmatizator:
    "Lemmatizes yes"
    def __init__(self, modelpath: str = 'czech-morfflex2.0-pdtc1.0-220710-pos_only.tagger') -> None:
        """Initializes the language model, singleton"""

        # Path to the Czech model
        self.tagger = ufal.morphodita.Tagger.load(modelpath)
        if not self.tagger:
            raise Exception("Cannot load the tagger model!")

        # Create forms and lemmas
        self.forms = ufal.morphodita.Forms()
        self.lemmas = ufal.morphodita.TaggedLemmas()

    def tokenize(self, text: str) -> list[str]:
        """Tokenizes the text (splits it, but also removes white space symbols)"""
        tokenized_text = nltk.word_tokenize(text)
        print("tokenized text:", tokenized_text)
        return tokenized_text
    
    def lemmatize(self, text: str) -> str:
        """Lemmatizes the text with newlines as the delimeter"""
        text = self.tokenize(text)

        lemmatized_words = []
        for word in text:
            if word == "\n":
                lemmatized_words.append(word)
            if re.match(r'^[^\w\s]+$', word):
                continue

            # Tag the word
            self.forms.clear()
            self.forms.push_back(word)
            self.tagger.tag(self.forms, self.lemmas)

            # Use the first lemma as the lemmatized word
            if len(self.lemmas) > 0:
                lemmatized_words.append(self.lemmas[0].lemma)
            else:
                lemmatized_words.append(word)  # If no lemma is found, keep the original word
        return lemmatized_words

    def print_info(self, text: str) -> None:
        """Prints every information, debug purposes"""
        lemmas = self.lemmatize(text)
        for idx in range(len(lemmas)):
            if lemmas[idx] == "\n": continue
            print(lemmas[idx])
            print("---")

    def get_lemmas(self, text: str) -> list[str]:
        """returns a list containing readable lemmas (without additional information)"""
        lemmas = self.lemmatize(text)
        formatted_lemmas = []
        for lemma in lemmas:
            for idx in range(len(lemma)):
                if lemma[idx] in ("_", "-", "'", "`"):
                    lemma = lemma[:idx]
                    break
            formatted_lemmas.append(lemma)
        return formatted_lemmas

lemmatizator = Lemmatizator()
    
if __name__ == "__main__":
    # Text to be analyzed
    text1 =  """Kniha nás uvítá k životu na Panské farmě vlastněnou panem Jonesem
            který se ke zvířatům chová převážně krutě (až na nějaké vyjímky - klisně Molině podává cukr).
            Když je jednou Jones zapomene nakrmit, zvířata vzbudí revoluci a úspěšně odeženou Jonese pryč,
            čímž se osvobodí a přivlastní si farmu.""" 
    text2 = "Šel jsem do lesa a potkal dlažební kostku \n\n A byla úplně úžasná"
    text3 = """Knihu napsala Alice Feeney Britská spisovatelka tohoto století, která píše převážně mysteriózní knihy. Z angličtiny knihu přeložila Michaela Martinová.
            Literárním druhem je epika
            žánr je psychologický thriller a román. a pak jsem šel nakoupit vodu
            Kompozice je chronologická s prvky retrospektivy. 
            Kniha je psaná převážně v ich-formě
            Hlavním tématem knihy je nešťastné manželství a tajemství, které ho doprovází. V příběhu se nachází 3 hlavní postavy, kterým je okolo 40 let.
            hlavní vypravěč se neustále střídá mezi Adamem, Amélií a Robin. Takže vidíme u každé postavy jejich úhel pohledu a myšlenky
            """
    text4 = """Kočka leze dírou \n Pes oknem"""

    print(lemmatizator.print_info(text1))
    print(lemmatizator.get_lemmas(text2))
    print(lemmatizator.get_lemmas(text3))
    print(lemmatizator.get_lemmas(text4))