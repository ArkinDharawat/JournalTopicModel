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

journal_df = pd.read_csv(os.path.join(os.getcwd(), "../data/journalslist.csv"))

cnx = mysql.connector.connect(**config)
logger.info("Connected to SQL")

cursor = cnx.cursor()
logger.info("Created Cursor")

insert_query = SQLStrObj.insert_journal()
for id, row in journal_df.iterrows():
    name, journal_id, category = row.values
    cursor.execute(insert_query, (journal_id, name, category))
    cnx.commit()  # Commit one row at a time

cursor.close()
cnx.close()
logger.info("Connection Closed")
