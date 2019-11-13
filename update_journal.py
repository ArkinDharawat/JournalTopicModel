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

journal_id_rank_df = pd.read_csv(os.path.join("/home/project/data/JournalIdRank.csv"))

cnx = mysql.connector.connect(**config)
logger.info("Connected to SQL")

cursor = cnx.cursor()
logger.info("Created Cursor")

for id, row in journal_id_rank_df.iterrows():
    journal_id, rank = row.values
    cursor.execute("UPDATE Academic_Journal SET Rank=%s WHERE Journal_Id=%s", (rank, journal_id))
    cnx.commit()  # Commit one row at a time

cursor.close()
cnx.close()
logger.info("Connection Closed")
