from flask import Flask, request, jsonify
from app import app
import mysql.connector
import yaml
from SQLQueries.SQLStrQuery import SQLStrQuery

INSERT = "Insert"
DELETE = "Delete"
UPDATE = "Update"
SEARCH = "Search"
cnx = None
SQLStrObj = None
TopicModelobj = None
@app.before_first_request
def before_request_func():
    SQLStrObj = SQLStrQuery(10)
    with open(os.path.join(os.getcwd(), "../config.yml"), 'r') as stream:
        config = yaml.safe_load(stream)
    cnx = mysql.connector.connect(**config)
    TopicModelobj = TopicModel(os.path.join(os.path.expanduser('~'), "../../project/data/"))
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
    journal_id = str(request.form['journal_id'])
    cursor = cnx.cursor()
    insert_paper_query = SQLStrObj.insert_paper()
    topics = TopicModelobj.get_topics(title=title, abstract=abstract)
    insert_topic_query = SQLStrObj.insert_topic(paper_id, topics)
    try:
        cursor.execute(insert_paper_query, (paper_id, authors, journal_id, title, abstract))
        cursor.execute(insert_topic_query)
    except Exception as e:
        pass  
    cursor.close()

def delete_data(request):
    paper_id = str(request.form['paper_id'])

def update_data(request):
    paper_id = str(request.form['paper_id'])


def search_data(request):
    pass

