from flask import Flask, request, jsonify
from app import app


# static url
@app.route('/')
def index():
    return "Hello World!"

# url parameters
@app.route('/endpoint/<input>')
def endpoint(input):
    return input

# api with endpoint
@app.route('/Hashtag', methods=['GET'])
def nameEndpoint():
    if 'aaa' in request.args:
    	return jsonify(a)
    elif 'name' in request.args:
        return "YAY"
