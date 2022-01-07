from ie import get_response

from flask import Flask
app = Flask(__name__)

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/query-example')
def query_example():
    language = request.args.get('article_content')
    return get_response(language)

@app.route('/post', methods=["POST"])
def testpost():
     input_json = request.get_json(force=True)
     dictToReturn = {'text':input_json['text']}
     return jsonify(dictToReturn)