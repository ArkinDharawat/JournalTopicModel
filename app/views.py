from flask import Flask, request, jsonify
from app import app
import mysql.connector
import yaml
from SQLQueries.SQLStrQuery import SQLStrQuery

INSERT = "Insert"
DELETE = "Delete"
UPDATE = "Update"
SEARCH = "Search"
@app.before_first_request
def before_request_func():

# static url
@app.route('/')
def index():
    return render_template('templates/index.html')

@app.route('/query', methods=['POST'])
def insert_endpoint():
    action = str(request.form.get('action'))
    if action == INSERT:
        pass
    elif action == DELETE:
        pass
    elif action == UPDATE:
        pass
    elif action == SEARCH:
        pass

def insert_data(request):
    paper_id = str(request.form['paper_id'])
    authors = str(request.form['authors'])
    title = str(request.form['title'])
    abstract = str(request.form['abstract'])

def delete_data(request):
    paper_id = str(request.form['paper_id'])

def update_data(request):
    paper_id = str(request.form['paper_id'])


def search_data(request):
    pass

