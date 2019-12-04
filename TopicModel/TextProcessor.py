import nltk
import spacy

import re

spacy.load('en_core_web_sm')  # OR spacy.load('en_core_web_sm')
# Instructions to install the spaCy English model
""" 
python -m spacy download en 
OR 
python3 -m pip install --user https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz
"""

from spacy.lang.en import English

parser = English()  # English parser

if "stopwords" not in dir(nltk.corpus):
    nltk.download('stopwords')  # Download NLTK stopwords
en_stop = set(nltk.corpus.stopwords.words('english'))


def remove_non_ascii(text):
    """ Clean up text to support characters
    Args:
        text: string of text
    Returns: cleaned text
    """
    if isinstance(text, float):
        return ""
    return re.sub(r'[^\x00-\x7F]+', ' ', text)


def tokenize(text):
    """ Remove stopwords and spaces from text to get tokens for model
    Args:
        text: string of text
    Returns: List of tokens
    """
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens


def prepare_text_for_lda(text):
    """ Prepare text before training LDA model
    Args:
        text: string of text
    Returns: cleaned tokens
    """
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    return tokens


def apply_tokenization(title, abstract):
    """ Tokenize text for title + abstract
    Args:
        title: title of the paper
        abstract: abstract of the paper
    Returns: cleaned tokens
    """
    word = ""
    word += remove_non_ascii(title)
    word += remove_non_ascii(abstract)
    return prepare_text_for_lda(word)
