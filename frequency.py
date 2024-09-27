import csv

class WordProperties:
    """simplyfing the properties of the word"""
    def __init__(self, name, freq, sf, bf, of, pf, character=None):
        self.freq = int(freq)
    
    def __eq__(self, value: object) -> bool:
        return self.name == value
    
    def __hash__(self) -> int:
        return hash(self.name)
    
    def __contains__(self, item) -> bool:
        return self == item


class Corpus:
    """initializes the frequency data"""
    def __init__(self) -> None:
        self.words = dict()
        with open("syn2015_lemma_utf8.tsv", "r") as csv_file:
            contents = csv.reader(csv_file, delimiter="\t")
            for word in contents:
                name = word[1].lower()
                info = word[2:]
                if len(name) > 3 and name not in self.words:
                    self.words[name] = WordProperties(*info)
    def get_words(self):
        """getter"""
        return self.words
    def print_info(self) -> None:
        """returns the word and its frequency, debug purposes"""
        print(sorted([(name, properties.freq) for name, properties in self.words.items()], key=lambda x: x[1]))

corpus = Corpus()

if __name__ == "__main__":
    corpus.print_info()
    words = corpus.get_words()
    print("kočka" in words)
