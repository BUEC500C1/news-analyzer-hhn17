from flask import request, make_response, Flask
import flask
import config as conf
import logging
import os
import json
import util
import mongo_operation
from datetime import datetime
from uuid import uuid4

logging.basicConfig(level=logging.DEBUG)

api = Flask(__name__)

@api.route('/api/v1/keywordSearch',methods=['POST'])
def keywordSearch():
    try:
        data = request.get_json()
    except Exception as exp:
        logging.error("Got error in feteching json data {}".format(str(exp)))  
    #data = {"Author": session['author'], "AuthorID": session['author_id'], "keyword": key}
    '''
     mong_record['Author'] = data['Author']
    mong_record['AuthorID'] = data['AuthorID']
    '''
    db_con = mongo_operation.get_db_conn()
    file_id, access = mongo_operation.full_text_search(data, db_con)
    return flask.jsonify({"file_id":file_id,"access_id":access})

@api.route('/api/v1/getText',methods=['POST'])
def getttextt():
    try:
        data = request.get_json()
    except Exception as exp:
        logging.error("Got error in feteching json data {}".format(str(exp)))  
    
    db_con = mongo_operation.get_db_conn()
    output = mongo_operation.search_on_id(data, db_con)
    return flask.jsonify({"content":output})


@api.route('/api/v1/login',methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # file metadata
    except Exception as exp:
        logging.error("Got error in feteching json data {}".format(str(exp)))
        
    author_name = data['author_name']
    author_id = data['author_id']
    
    mong_record = {}
    mong_record['Author'] = author_name 
    mong_record['Author_ID'] = author_id
    db_con = mongo_operation.get_db_conn()
    res = mongo_operation.search(mong_record,db_con)
    result = dict()
    
    if res == 0:
        result['authorize'] = 0
    else:
        result['authorize'] = 1
    return flask.jsonify(result)

@api.route('/api/v1/signup',methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        # file metadata
    except Exception as exp:
        logging.error("Got error in feteching json data {}".format(str(exp)))
        
    author_name = data['author_name']
    author_id = str(uuid4())
    
    mong_record = {}
    mong_record['Author'] = author_name 
    mong_record['Author_ID'] = author_id
    db_con = mongo_operation.get_db_conn()
    res = mongo_operation.register(mong_record,db_con)
    result = {"author_id":author_id}
    
    return flask.jsonify(result)
      
if __name__ == '__main__':
    api.run(host="0.0.0.0", port=5115, debug=True)

