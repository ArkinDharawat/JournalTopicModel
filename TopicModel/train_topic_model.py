import os
import pickle

import gensim
import pandas as pd
from TextProcessor import apply_tokenization_row
from gensim import corpora, models

NUM_TOPICS = 10
MULTICORE = True
MODEL_FOLDER = "/home/project/data"


def build_data():
    # read df
    df_chunked = pd.read_csv("/home/project/data/AllArticles_Subset.csv")
    text_data = df_chunked.apply(lambda x: apply_tokenization_row(x), axis=1)

    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]

    tfidf = models.TfidfModel(corpus, id2word=dictionary)

    low_value = 0.5
    low_value_words = []
    for bow in corpus:
        low_value_words += [(id, dictionary[id]) for id, value in tfidf[bow] if value < low_value]

    dictionary.filter_tokens(bad_ids=low_value_words)
    corpus = [dictionary.doc2bow(doc) for doc in text_data]  # Recompute corpus

    pickle.dump(corpus, open(os.path.join(MODEL_FOLDER, 'corpus.pkl'), 'wb'))
    dictionary.save(os.path.join(MODEL_FOLDER, 'dictionary.gensim'))


def run_model():
    dictionary = gensim.corpora.Dictionary.load(os.path.join(MODEL_FOLDER, 'dictionary.gensim'))
    corpus = pickle.load(open(os.path.join(MODEL_FOLDER, 'corpus.pkl'), 'rb'))
    model_params = {"corpus": corpus,
                    "num_topics": NUM_TOPICS,
                    "id2word": dictionary,
                    "passes": 10,
                    "random_state": 42}
    if MULTICORE:
        ldamodel = gensim.models.ldamulticore.LdaMulticore(**model_params)
    else:
        ldamodel = gensim.models.ldamodel.LdaModel(**model_params)

    ldamodel.save(os.path.join(MODEL_FOLDER, 'model5.gensim'))

if __name__ == '__main__':
    build_data()
    run_model()
