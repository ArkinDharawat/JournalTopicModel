import pickle
import gensim
import os
from TopicModel.TextProcessor import apply_tokenization


class TopicModel(object):
    def __init__(self, model_folder):
        self.dictionary = gensim.corpora.Dictionary.load(
            os.path.join(model_folder, 'dictionary.gensim'))  # model-words dictioanry
        self.corpus = pickle.load(open(os.path.join(model_folder, 'corpus.pkl'), 'rb'))  # model corpus. Not needed
        self.ldamodel = gensim.models.ldamodel.LdaModel.load(os.path.join(model_folder, 'model5.gensim'))  # LDA model

    def __str__(self):
        return "TopicModel"

    def get_topics(self, title, abstract):
        """ Get the topics given title and abstract
        Args:
            title: the title of the paper
            abstract:  the abstract of the paper
        Returns: List of topics that are present
        """
        text = apply_tokenization(title, abstract)  # Apply tokenization
        text_doc_bow = self.dictionary.doc2bow(text)  # make bag of words
        topics = self.ldamodel.get_document_topics(text_doc_bow)  # Get topics
        return [x[0] for x in topics]


if __name__ == '__main__':
    obj = TopicModel("/Users/arkin/Desktop/CS411/project/data")
    topics = obj.get_topics(title="General Equilibrium Impacts of a Federal Clean Energy Standard",
                            abstract="General Equilibrium Impacts of a Federal Clean Energy Standard")
    print(topics)
