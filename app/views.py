from flask import Flask, request, jsonify, render_template, g
from app import app
import mysql.connector
import yaml
import os
from SQLQueries.SQLStrQuery import SQLStrQuery

from TopicModel.TopicExtractor import TopicModel
from TopicModel.TextProcessor import remove_non_ascii

import os

INSERT = "Insert"
DELETE = "Delete"
UPDATE = "Update"
SEARCH = "Search"



@app.before_first_request
def before_first_request_func():
    print("Here?")


@app.before_request
def before_request_func():
    g.SQLStrObj = SQLStrQuery(10)
    g.TopicModelobj = TopicModel(os.path.join(os.path.expanduser('~'), "../project/data/"))
    with open(os.path.join(os.getcwd(), "config.yaml"), 'r') as stream:
        config = yaml.safe_load(stream)
    g.cnx = mysql.connector.connect(**config)
    g.cursor = g.cnx.cursor()



# static url
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/query', methods=['POST'])
def insert_endpoint():
    action = str(request.form.get('action'))

    if action == INSERT:
        insert_data(request)
        return render_template('insert_successful.html')
    elif action == DELETE:
        delete_data(request)
        return render_template('delete_successful.html')

    elif action == UPDATE:
        update_data(request)
        return render_template('update_successful.html')
    # elif action == SEARCH:
    #     search_data(request)


def insert_data(request):
    SQLStrObj = g.SQLStrObj
    TopicModelobj = g.TopicModelobj
    cursor = g.cursor
    cnx = g.cnx

    paper_id = str(request.form['paper_id'])
    authors = str(request.form['authors'])
    title = str(request.form['title'])
    abstract = str(request.form['abstract'])
    journal_id = str(request.form['journal_id'])

    title = remove_non_ascii(title)
    abstract = remove_non_ascii(abstract)

    insert_paper_query = SQLStrObj.insert_paper()

    topics = TopicModelobj.get_topics(title=title, abstract=abstract)

    insert_topic_query = SQLStrObj.insert_topic(paper_id, topics)
    try:
        cursor.execute(insert_paper_query, (paper_id, authors, journal_id, title, abstract))
        cursor.execute(insert_topic_query)
    except Exception as e:
        return "Error :" + str(e)
    cnx.commit()

    return "INSERTION SUCCESSFULL"


def delete_data(request):
    SQLStrObj = g.SQLStrObj
    cursor = g.cursor
    cnx = g.cnx

    paper_id = str(request.form['paper_id'])
    delete_paper_query = SQLStrObj.delete_paper()
    delete_topic = SQLStrObj.delete_topic()
    try:
        cursor.execute(delete_topic, (paper_id,))
        cursor.execute(delete_paper_query, (paper_id,))
    except Exception as e:
        return "Error :" + str(e)
    cnx.commit()

    return "DELETION SUCCESSFULL"


def filter_update_data(request):
    default = "Default"
    data_map = {}
    # data = []

    authors = str(request.form['authors'])
    if authors != default:
        data_map["authors"] = authors
        # data.append(authors)

    title = str(request.form['title'])
    if title != default:
        data_map["title"] = title
        # data.append(title)
    abstract = str(request.form['abstract'])
    if abstract != default:
        data_map["abstract"] = abstract
        # data.append(abstract)

    journal_id = str(request.form['journal_id'])
    if journal_id != default:
        data_map["journal_id"] = journal_id
        # data.append(journal_id)

    return data_map


def update_data(request):
    SQLStrObj = g.SQLStrObj
    cursor = g.cursor
    cnx = g.cnx

    paper_id = str(request.form['paper_id'])
    data_map= filter_update_data(request)
    if column != [] and data != []:
        data = list(data_map.values())
        data.append(paper_id)
        data = tuple(data)
        update_query = SQLStrObj.update_paper
        try:
            cursor.execute(list(data_map.keys()), data) ##order might not be ensured here
            # TODO: Add query to update topic
        except Exception as e:
            return "Error :" + str(e)
        cnx.commit()
    return "UPDATE SUCCESSFULL"


def search_data(request):
    pass


@app.after_request
def after_request_func(response):
    g.cursor.close()
    g.cnx.close()
    return response
