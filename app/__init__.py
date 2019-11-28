from flask import Flask
import sys

app = Flask(__name__)
app.config['database'] = sys.argv[1]
from app import views
