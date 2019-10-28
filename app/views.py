from flask import Flask, request, jsonify
from app import app


# static url
@app.route('/')
def index():
    return "Hello World!"

@app.route('/insert', methods=['POST'])
def insert_endpoint():
    paper_id = request.form['paper_id']
    authors = request.form['authors']
    journal_id = request.form['journal_id']
    title = request.form['title']
    abstract = request.form['abstract']
    


@app.route('/insert', methods=['POST'])
def update_endpoint():
    pass

@app.route('/insert', methods=['POST'])
def delete_endpoint():
    pass