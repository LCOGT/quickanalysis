from flask import Flask
application = app = Flask(__name__)


from flask import Flask, request, jsonify
import json

from quickanalysis.utils import hello_world
from quickanalysis.analysis.fakes import emptylist


@app.route('/', methods=['GET', 'POST'])
def home():
    return jsonify({"data":""})


@app.route('/empty', methods=['GET'])
def empty_route():
    return jsonify({
        "data": emptylist()
    })

"""
@app.route('/submit', methods=['POST'])
def submit():
    form_submission = json.loads(request.form['data'])
    return jsonify({
        "form_submission": form_submission,
        })

Send a POST with form data:
curl -X POST http://localhost:5000/submit -F 'data={"key1":"val1"}'
"""

if __name__ == "__main__":
    application.run()
