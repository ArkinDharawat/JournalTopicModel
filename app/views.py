from flask import Flask, request, jsonify
from app import app
import mysql.connector
import yaml
from SQLQueries.SQLStrQuery import SQLStrQuery
import os
from TopicModel.TopicExtractor import TopicModel


INSERT = "Insert"
DELETE = "Delete"
UPDATE = "Update"
SEARCH = "Search"
# cnx = None
# SQLStrObj = None
# TopicModelobj = None
# cursor = None
@app.before_first_request
def before_request_func():
    SQLStrObj = SQLStrQuery(10)
    with open(os.path.join(os.getcwd(), "config.yaml"), 'r') as stream:
        config = yaml.safe_load(stream)
    cnx = mysql.connector.connect(**config)
    TopicModelobj = TopicModel( "/home/project/data")
    cursor = cnx.cursor()
# static url
@app.route('/')
def index():
    return render_template('templates/index.html')

@app.route('/query', methods=['POST'])
def insert_endpoint():
    action = str(request.form.get('action'))
    if action == INSERT:
        insert_data(request)
    elif action == DELETE:
        delete_data(request)
    elif action == UPDATE:
        update_data(request)
    elif action == SEARCH:
        search_data(request)

def insert_data(request):
    paper_id = str(request.form['paper_id'])
    authors = str(request.form['authors'])
    title = str(request.form['title'])
    abstract = str(request.form['abstract'])
    journal_id = str(request.form['journal_id'])
    insert_paper_query = SQLStrObj.insert_paper()
    topics = TopicModelobj.get_topics(title=title, abstract=abstract)
    insert_topic_query = SQLStrObj.insert_topic(paper_id, topics)
    try:
        cursor.execute(insert_paper_query, (paper_id, authors, journal_id, title, abstract))
        cursor.execute(insert_topic_query)
    except Exception as e:
        pass  

def delete_data(request):
    paper_id = str(request.form['paper_id'])
    delete_paper_query = SQLStrObj.delete_paper()
    try:
        cursor.execute(delete_paper_query, paper_id)
    except Exception as e:
        pass
def filter_update_data(request):
    default = "Default"
    column = []
    data = []

    authors = str(request.form['authors']) 
    if authors != default: 
        column.append("authors")
        data.append(authors)
    title = str(request.form['title'])
    if title != default: 
        column.append("title")
        data.append(title)
    abstract = str(request.form['abstract'])
    if abstract != default: 
        column.append("abstract")
        data.append(abstract)
    journal_id = str(request.form['journal_id'])
    if journal_id != default: 
        column.append("journal_id")
        data.append(journal_id)
    return column, data
def update_data(request):
    paper_id = str(request.form['paper_id'])
    column, data = filter_update_data(request)
    if column != [] and data != []:
        data.append(paper_id)
        data = tuple(data)
        update_query = SQLStrObj.update_paper
        try:
            cursor.execute(update_query, data)
        except Exception as e:
            pass

def search_data(request):
    pass



