import logging
import os

import mysql.connector
import yaml
from SQLQueries.SQLStrQuery import SQLStrQuery

logger = logging.getLogger("ddl-script")

SQLStrObj = SQLStrQuery(10)  # TODO: Change to global var

# Read YAML file
with open(os.path.join(os.getcwd(), "config.yml"), 'r') as stream:
    config = yaml.safe_load(stream)

cnx = mysql.connector.connect(**config)
logger.info("Connected to SQL")

cursor = cnx.cursor()
logger.info("Created Cursor")

for ddl_query_str in SQLStrObj.create_tables():
    cursor.execute(ddl_query_str)
logger.info("Created tables")

stored_procedure = SQLStrObj.create_procedure()
cursor.execute(stored_procedure)


cursor.close()
cnx.close()

logger.info("All Connections Closed")
