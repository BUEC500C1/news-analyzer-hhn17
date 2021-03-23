from uuid import uuid4
import logging
import requests
import config
import json

def get_sentiment(cont):
    """
    Fetch the sentiment score from api created for google nlp
    """
    data = dict()
    data['content'] = cont
    header_conf = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(config.sentiment_api, data=json.dumps(data), headers=header_conf)
    return response.json()