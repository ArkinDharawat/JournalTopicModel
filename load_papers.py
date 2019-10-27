import pandas as pd
import logging
import os

import mysql.connector
import yaml
from SQLQueries.SQLStrQuery import SQLStrQuery
from TopicModel.TopicExtractor import TopicModel

import re

def remove_non_ascii(text):
    if  isinstance(text, float):
        return ""
    return re.sub(r'[^\x00-\x7F]+',' ', text)

logger = logging.getLogger("load-journal-sql")

SQLStrObj = SQLStrQuery(10)  # TODO: Change to global var
TopicModelobj = TopicModel(os.path.join(os.path.expanduser('~'), "../project/data/"))

# Read YAML file
with open(os.path.join(os.getcwd(), "config.yml"), 'r') as stream:
    config = yaml.safe_load(stream)

chunksize = 10 ** 3
df_full = pd.read_csv(os.path.join(os.path.expanduser('~'), "../project/data/AllArticles.csv"), chunksize=chunksize, header=None)

cnx = mysql.connector.connect(**config)
logger.info("Connected to SQL")

cursor = cnx.cursor()
logger.info("Created Cursor")

insert_paper_query = SQLStrObj.insert_paper()

i = 10
for chunk in df_full:
    if i > 10:
        break

    df_chunked = chunk.iloc[:, [1, 2, 10, 13]]
    df_chunked.columns = ["title", "author", "abstract", "journal_id"]
    for id, row in df_chunked.iterrows():
        title, author, abstract, journal_id = row.title, row.author, row.abstract, row.journal_id
        title = remove_non_ascii(title)
        abstract = remove_non_ascii(abstract)

        topics = TopicModelobj.get_topics(title=title, abstract=abstract)
        try:
            insert_topic_query = SQLStrObj.insert_topic(id, topics)
            cursor.execute(insert_paper_query, (id, author, journal_id, title, abstract))
            cursor.execute(insert_topic_query)
        except Exception as e:
            logger.debug("Failed at {0} with exception {1}".format(str(id), e))
        # cnx.commit()  # Commit one row at a time
    i += 1

cursor.close()
cnx.close()
logger.info("Connection Closed")
