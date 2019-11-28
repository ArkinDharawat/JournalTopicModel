from argparse import ArgumentParser

from flask import Flask

parser = ArgumentParser()
parser.add_argument('-db_type', default="sql")
args = parser.parse_args()

app = Flask(__name__)
if args.db_type not in ["sql", "neo4j"]:
    args.db_type = "sql"
app.config['database'] = args.db_type
