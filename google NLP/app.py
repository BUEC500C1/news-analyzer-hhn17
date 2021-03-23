from flask import request, make_response, Flask
import flask
import config as conf
import logging
import os
import json
from util import get_sentiments
#import tracemalloc


logging.basicConfig(level=logging.DEBUG)

api = Flask(__name__)


@api.route('/api/v1/getSentiment',methods=['POST'])
def get_sentiment():
    
    
    try:
        data = request.get_json()
    except Exception as e:
        logging.error("error in decoding data coming through request, the error message is {}".format(str(e)))
        
    text =  data['content']
    logging.debug("data is {}".format(text))
    outcome = get_sentiments(text)
    logging.debug(outcome)
    

    return flask.jsonify({"results":outcome})
        

if __name__ == '__main__':
    api.run(host="0.0.0.0", port=8118, debug=True)
    
