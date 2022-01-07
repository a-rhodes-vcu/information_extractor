from ie import get_response

from flask import Flask
app = Flask(__name__)

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/cleopatra', methods=["POST"])
def cleopatra():
    try:
        json_data = request.json
        content = json_data['article_content']
        question = json_data['question']
        return get_response(content,question)
    except:
        return "Error processing request"

@app.route('/post', methods=["POST"])
def testpost():
     input_json = request.get_json(force=True)
     dictToReturn = {'text':input_json['text']}
     return jsonify(dictToReturn)
