from ie import get_response

from flask import Flask
app = Flask(__name__)

from flask import Flask, request, jsonify

app = Flask(__name__)
import json
@app.route('/cleopatra')
def cleopatra():

    content = request.args.get('article_content')
    question = request.args.get('question')
    try:
        return get_response(content,question)
    except:
        return "Error processing request"

@app.route('/post', methods=["POST"])
def testpost():
     input_json = request.get_json(force=True)
     dictToReturn = {'text':input_json['text']}
     return jsonify(dictToReturn)
