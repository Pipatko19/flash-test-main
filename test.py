import re

def find_word_indexes(text):
    word_indexes = []
    # Adjust pattern to include hyphens and periods within words
    pattern = r'\b[\w.-]+(?:[\w.-]+)*\b'
    for match in re.finditer(pattern, text):
        start_index = match.start()
        end_index = match.end() - 1  # End index should be inclusive
        word_indexes.append((start_index, end_index))
    return word_indexes

# Example usage
text = "   Hello, world! This is a test. - těžko-oděnec 3.5"
print(find_word_indexes(text))
for start, end in find_word_indexes(text):
    print(text[start:end + 1])