from flask import Flask
import sys


app = Flask(__name__)
from app import views
if len(sys.argv) < 4:
    app.config['db_type'] = "sql"
elif sys.argv[3] not in ["sql", "neo"]:
    app.config['db_type'] = "sql"
else:
    app.config['db_type'] = sys.argv[3]