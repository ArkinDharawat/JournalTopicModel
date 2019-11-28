from flask import Flask
import sys


app = Flask(__name__)
from app import views
app.config.from_envvar('DB_TYPE')