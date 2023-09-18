from flask import Flask, request, jsonify 
from serviceslib import regex_service

app = Flask(__name__)

# services initialization
regex_service = regex_service.RegexService()

@app.route("/regex", methods=['GET','POST'])
def get_keywords():
    request_data = request.get_json()
    #print('request: ', request_data)
    #print("Getting keywords - REGEX service")
    #print("TEXT: ", request_data['jobDescription'])
    keywords_list = regex_service.get_keywords(request_data['jobDescription'])
    return jsonify({'keywords':keywords_list})

if __name__ == '__main__':
    port = 8910
    print("Running my app on port 8910")
    app.run(host="0.0.0.0",debug=True, port=port)