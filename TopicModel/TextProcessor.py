import nltk
import spacy

spacy.load('en')
# python -m spacy download en
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
