
# coding: utf-8

# In[1]:


import pandas as pd 


# In[96]:


chunksize = 10 ** 3
df_full = pd.read_csv("AllArticles.csv", chunksize=chunksize, header=None)
journal_df = pd.read_csv("journalslist.csv")


# In[97]:


i = 0
for chunk in df_full:
    df_chunked = chunk.iloc[:, [1, 2, 9, 10, 13]]
    df_chunked.columns = ["title", "author", "url", "abstract", "journal_id"]
    i+=1
    if i == 10:
        break


# In[98]:


# journal_df[journal_df["journal_id"]==1]["journal"].values[0]
df_chunked["field"] = df_chunked["journal_id"].apply(lambda x: journal_df[journal_df["journal_id"]==x]["field"].values[0])


# In[99]:


df_chunked


# In[133]:


import gensim
import spacy
# https://towardsdatascience.com/topic-modelling-in-python-with-nltk-and-gensim-4ef03213cd21


# In[106]:


spacy.load('en')
# python -m spacy download en
from spacy.lang.en import English
parser = English()
def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens


# In[107]:


import nltk
nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))


# In[108]:


def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    return tokens


# In[124]:


def apply_tokenization(r):
    title = r["title"]
    abstract = r["abstract"]
    word = ""
    if not isinstance(title, float):
        word += title 
    if not isinstance(abstract, float):
        word += abstract
    return prepare_text_for_lda(word)


# In[125]:


text_data = df_chunked.apply(lambda x: apply_tokenization(x), axis=1)


# In[128]:


# Prolly optimize this 
from gensim import corpora
dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]
import pickle
pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dictionary.gensim')


# In[131]:


import gensim
NUM_TOPICS = 10
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
# ldamodel.save('model5.gensim')
topics = ldamodel.print_topics(num_words=4)
for topic in topics:
    print(topic)


# In[132]:


import pyLDAvis.gensim
lda_display = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary, sort_topics=False)
pyLDAvis.display(lda_display)

