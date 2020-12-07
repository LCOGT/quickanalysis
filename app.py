
from flask import Flask, request, jsonify
import json

from utils import hello_world
from analysis.fakes import emptylist

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return jsonify({"two":two()})

@app.route('/submit', methods=['POST'])
def submit():
    form_submission = json.loads(request.form['data'])
    return jsonify({
        "form_submission": form_submission,
        })

@app.route('/empty', methods=['GET'])
def empty_route():
    return jsonify({
        "data": emptylist()
    })

"""
Send a POST with form data:
curl -X POST http://localhost:5000/submit -F 'data={"key1":"val1"}'
"""
