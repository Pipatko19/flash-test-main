import re

def _find_word_indices(text):
    word_indexes = []
    pattern = r'\b[\w.-]+(?:[\w.-]+)*\b'  # Pattern for words with hyphens and decimal points

    i = 0  # Position tracker
    while i < len(text):
        if text[i] == '\n':
            # Special action when encountering \n
            # # Mark the newline with its index
            i += 1
        else:
            # Check for word using the regex pattern from the current position
            match = re.match(pattern, text[i:])
            if match:
                start_index = i
                end_index = i + len(match.group())  
                word_indexes.append((start_index, end_index))
                i = end_index + 1  # Move to the next character after the word
            else:
                i += 1  # Move forward if no match
    print(word_indexes)
    return word_indexes

# Example usage
text = """kontinentalita = je-li území více vzdálené od oceánu, je kontinentalita vyšší = méně srážek (a obráceně) →
Vzdušné proudění - severní 
JZ USA + Západní pobřeží (pobřežní hory) - 3800 mm/m2
Západ amazonské nížiny + SV brazílie + francouzské guiney + JZ Patagonie - 8990 mm (kolumbie)
Mořské proudy
plovoucí led teče pomocí Labradorského studeného proudu na jih (až 40° s. z. š.)
Golfský proud, Severní tichomořský proud - teplé
Kalifornský proud - studený, způsobuje mohavskou poušť, sonorskou poušť
fun fact? Titanic ve střetu labradorského (ledovec) a golfského (tvoření mlhy), - tento střet také rybařiště (více vzduchu) - tresky"""
print(*(text[start:end] for start, end in _find_word_indices(text)))