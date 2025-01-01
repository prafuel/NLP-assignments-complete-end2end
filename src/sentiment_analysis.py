
from string import punctuation
from src.stopwords_list import get_stop_words_fn
from src.master_dict import pos_words, neg_words
import pandas as pd

import spacy
import pyphen
import re

import nltk
from nltk.corpus import stopwords

from textstat import syllable_count

# Ensure NLTK data is downloaded
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")


stopwords_dir = get_stop_words_fn()

# Define stopwords and punctuation
stopwords_nltk = set(stopwords.words('english'))


def removing_stopwords_fn(item: str) -> str:
    # removed stopwords from given data and punctuations
    stopwords_removed = " ".join(
        [s for s in nltk.word_tokenize(item)
            if s not in stopwords_dir and s not in punctuation
            and s not in stopwords_nltk
        ]
    )
    return stopwords_removed

def get_score_fn(row: str) -> str:
    """
    take row text as input and return pos_score | neg_score | neutral_score
    """
    pos_dict = []
    neg_dict = []
    neutral = []

    for item in row.split(" "):
        if item in pos_words:
            pos_dict.append(item)
        elif item in neg_words:
            neg_dict.append(item)
        else:
            neutral.append(item)

    pos_score = pd.Series(pos_dict).value_counts().sum()
    neg_score = pd.Series(neg_dict).value_counts().sum()
    neutral_score = pd.Series(neutral).value_counts().sum()
    
    return str(pos_score) + "|" + str(neg_score) + "|" + str(neutral_score)
    
def polarity_score_fn(score: str):
    pos, neg, neutral = score.split("|")

    pos_score = int(pos)
    neg_score = int(neg)
    
    polarity_score = (pos_score - neg_score) / ((pos_score + neg_score) + 0.000001)
    # print("polarity_score", polarity_score)

    return polarity_score

def subjectivity_score_fn(score: str):
    pos, neg, neutral = score.split("|")

    pos_score = int(pos)
    neg_score = int(neg)
    neutral_score = int(neutral)
    
    total_words = pos_score + neg_score + neutral_score
    subjectivity_score = (pos_score + neg_score) / (total_words + 0.000001)

    return subjectivity_score


def get_num_of_sentences_fn(text: str) -> int:
    doc = nlp(text)
    return len(list(doc.sents))

def get_num_of_complex_words_fn(text: str) -> int:
    dic = pyphen.Pyphen(lang='en')  # Initialize Pyphen for English
    words = text.split()  # Split text into words
    complex_words = [word for word in words if len(dic.inserted(word).split('-')) > 2]
    return len(complex_words)

def count_syllables_per_word_fn(text: str) -> list:
    text = text.lower()
    # num_of_syllables = [len(re.findall(r'[aeiouy]+', word)) for word in text.split(" ")]
    num_of_syllables = [syllable_count(word) for word in text.split(" ")]
    return num_of_syllables


def count_personal_pronouns_fn(text: str) -> int:
    # Define regex for personal pronouns
    personal_pronouns = r'\b(I|we|my|ours|us)\b'
    
    # Use regex to find all matches (case-insensitive)
    matches = re.findall(personal_pronouns, text, flags=re.IGNORECASE)
    
    # Exclude occurrences of "US" as the country
    filtered_matches = [match for match in matches if match.lower() != "us" or not is_country_us(text, match)]
    
    return len(filtered_matches)

def is_country_us(text: str, word: str) -> bool:
    """
    Checks if 'US' in the text refers to the country based on context.
    For simplicity, consider 'US' as the country if preceded by 'the' (case-insensitive).
    """
    pattern = r'\bthe\s+US\b'
    return bool(re.search(pattern, text, flags=re.IGNORECASE))