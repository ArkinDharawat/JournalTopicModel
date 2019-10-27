import nltk
import spacy

spacy.load('en_core_web_sm')  # OR spacy.load('en_core_web_sm')
""" 
python -m spacy download en 
OR 
python3 -m pip install --user https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz
"""

from spacy.lang.en import English

parser = English()

if "stopwords" not in dir(nltk.corpus):
    nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))


def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens


def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    return tokens


def apply_tokenization(title, abstract):
    word = ""
    if not isinstance(title, float):
        word += title
    if not isinstance(abstract, float):
        word += abstract
    return prepare_text_for_lda(word)
