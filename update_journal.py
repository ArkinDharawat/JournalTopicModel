import pandas as pd
import logging
import os

import mysql.connector
import yaml
from SQLQueries.SQLStrQuery import SQLStrQuery

logger = logging.getLogger("load-journal-sql")

SQLStrObj = SQLStrQuery(5)  # TODO: Change to global var

# Read YAML file
with open(os.path.join(os.getcwd(), "config.yml"), 'r') as stream:
    config = yaml.safe_load(stream)


"""
df = pd.read_csv("/home/project/data/JournalRankings.csv")
df1 = pd.read_csv("/home/project/data/journalslist.csv")
jounral_id_rankings = df1.merge(df,  left_on='journal', right_on='journal_name')
journal_rankings = jounral_id_rankings[["journal_id", "ranking"]].groupby(by="journal_id").max()
"""

journal_id_rank_df = pd.read_csv(os.path.join("/home/project/data/JournalIdRankings.csv"))

cnx = mysql.connector.connect(**config)
logger.info("Connected to SQL")

cursor = cnx.cursor()
logger.info("Created Cursor")

for id, row in journal_id_rank_df.iterrows():
    journal_id, rank = row.values
    cursor.execute("UPDATE Academic_Journal SET Rank = %s WHERE Journal_Id = %s", (rank, journal_id))
    cnx.commit()  # Commit one row at a time

cursor.close()
cnx.close()
logger.info("Connection Closed")
