from flask import Flask, request, jsonify
from serviceslib import heuristic_service
from serviceslib import ml_service
import pandas as pd

app = Flask(__name__)

# services initialization
heuristic_service = heuristic_service.HeuristicService()
ml_service = ml_service.MLService()


@app.route("/heuristics", methods=['GET', 'POST'])
def get_keywords_heuristic():
    request_data = request.get_json()
    print('request: ', request_data)
    # print("Getting keywords - heuristic service")
    # print("TEXT: ", request_data['jobDescription'])
    keywords_list = heuristic_service.get_keywords(
        request_data['jobDescription'])
    return jsonify({'keywords': keywords_list})


@app.route("/ml", methods=['GET', 'POST'])
def get_keywords_ml():
    json_ = request.json
    print('received request')
    df = pd.DataFrame(json_, columns=model_columns)
    keywords_list = ml_service.get_keywords(df)
    print(keywords_list)
    return jsonify({'keywords': keywords_list})


if __name__ == '__main__':
    port = 8910
    model_columns = ['position', 'jobDescription']
    print("Running my app on port 8910")
    app.run(host="0.0.0.0", debug=True, port=port)
