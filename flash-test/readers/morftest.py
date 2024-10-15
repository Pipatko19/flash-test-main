import ufal.morphodita
import nltk
import re
nltk.download('punkt_tab')

class Lemmatizator:
    "Lemmatizes yes"
    def __init__(self, modelpath: str) -> None:
        """Initializes the language model"""

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

    
if __name__ == "__main__":
    lemmatizator = Lemmatizator()
    # Text to be analyzed
    text1 = """Vítr skoro nefouká a tak by se na první pohled mohlo zdát, 
            že se balónky snad vůbec nepohybují. Jenom tak klidně levitují ve vzduchu. 
            Jelikož slunce jasně září a na obloze byste od východu k západu hledali mráček marně, 
            balónky působí jako jakási fata morgána uprostřed pouště. Zkrátka široko daleko nikde nic, 
            jen zelenkavá tráva, jasně modrá obloha a tři křiklavě barevné pouťové balónky, 
            které se téměř nepozorovatelně pohupují ani ne moc vysoko, ani moc nízko nad zemí.
            """

    print(lemmatizator.print_info(text1))
