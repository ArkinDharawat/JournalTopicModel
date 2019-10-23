import pickle
import gensim
import os
from TextProcessor import apply_tokenization


class TopicModel(object):
    def __init__(self, model_folder):
        self.dictionary = gensim.corpora.Dictionary.load(os.path.join(model_folder, 'dictionary.gensim'))
        self.corpus = pickle.load(open(os.path.join(model_folder, 'corpus.pkl'), 'rb'))
        self.ldamodel = gensim.models.ldamodel.LdaModel.load(os.path.join(model_folder, 'model5.gensim'))

    def __str__(self):
        return "TopicModel"

    def get_topics(self, title, abstract):
        text = apply_tokenization(title, abstract)
        text_doc_bow = self.dictionary.doc2bow(text)
        topics = self.ldamodel.get_document_topics(text_doc_bow)
        return topics


if __name__ == '__main__':
    obj = TopicModel("/Users/arkin/Desktop/CS411/project/data")
    topics = obj.get_topics(title="General Equilibrium Impacts of a Federal Clean Energy Standard",
                            abstract="General Equilibrium Impacts of a Federal Clean Energy Standard")
    print(topics)
