import re
from symspellpy import SymSpell, Verbosity
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import spacy
import nltk

# Load necessary resources
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
sym_spell.load_dictionary("frequency_dictionary_en_82_765.txt", term_index=0, count_index=1)

stop_words = set(stopwords.words('english'))
ps = PorterStemmer()
nlp = spacy.load("en_core_web_sm")


# 1. Clean Query
def clean_query(query):
    # query = query.lower()
    query = re.sub(r'[^a-zA-Z0-9\s]', '', query)  # Remove special characters
    return query

# 2. Spell Correction
def correct_spelling(query):
    suggestions = sym_spell.lookup_compound(query, max_edit_distance=2)
    return suggestions[0].term if suggestions else query

# 3. Remove Stopwords
def remove_stopwords(query):
    words = query.split()
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

# 4. Stemming
def stem_query(query):
    words = word_tokenize(query)
    return ' '.join([ps.stem(word) for word in words])

# Preprocessing Pipeline
def preprocess_query(query):
    query = clean_query(query)
    query = correct_spelling(query)
    query = remove_stopwords(query)
    # query = stem_query(query)
    return query
