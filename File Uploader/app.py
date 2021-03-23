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


@api.route('/api/v1/textupload/uploadFile',methods=['POST'])
def upload():
    """Register user in database"""
    try:
        json_of_metadatas = request.form.to_dict(flat=False)
        data = json_of_metadatas['data'][0]
        data = json.loads(data)
        
        # file metadata
    except Exception as exp:
        logging.error("Got error in feteching json data {}".format(str(exp)))
        
    text = request.files['file'].read().decode("utf-8")
    sentiment = util.get_sentiment(text)['results']
    
    mong_record = {}
    # needs to add author ID
    mong_record['Author'] = data['Author']
    mong_record['AuthorID'] = data['AuthorID']
    mong_record['Upload time'] = datetime.now()
    mong_record['FILE_ID'] = str(uuid4())
    mong_record['content metadata'] = [{"sentiment":sentiment[0],"sentiment score":sentiment[1],"text":text}]
    db_con = mongo_operation.get_db_conn()
    logging.debug("Connection is fetched")
    mong_rec_id = mongo_operation.insert_record(mong_record, db_con)
    logging.debug(mong_rec_id.inserted_id)
    return flask.jsonify(json.dumps({"FILE_ID":mong_record['FILE_ID'],"mongo_rec_id":str(mong_rec_id.inserted_id), "status": "created"}))
    
@api.route('/api/v1/textupload/update',methods=['POST'])
def update_file():
    """Register user in database"""
    try:
        json_of_metadatas = request.form.to_dict(flat=False)
        data = json_of_metadatas['data'][0]
        data = json.loads(data)
        
        # file metadata
    except Exception as exp:
        logging.error("Got error in feteching json data {}".format(str(exp)))
        
    text = request.files['file'].read().decode("utf-8")
    sentiment = util.get_sentiment(text)['results']
    
    mong_record = {}
    # needs to add author ID
    mong_record['Author'] = data['Author']
    mong_record['Modified time'] = datetime.now()
    mong_record['FILE_ID'] = data['File_ID']
    mong_record['content metadata'] = [{"sentiment":sentiment[0],"sentiment score":sentiment[1],"text":text}]
    db_con = mongo_operation.get_db_conn()
    logging.debug("Connection is fetched")
    status = mongo_operation.update_record(mong_record, db_con)
    return flask.jsonify(json.dumps({"FILE_ID":mong_record['FILE_ID'], "status": "updated"}))

@api.route('/api/v1/textingester/delete',methods=['POST'])
def delete_file():
    """Register user in database"""
    try:
        data = request.get_json()
        #json_of_metadatas = request.form.to_dict(flat=False)
        #data = json_of_metadatas['data'][0]
        #data = json.loads(data)
        
        # file metadata
    except Exception as exp:
        logging.error("Got error in feteching json data {}".format(str(exp)))        
    mong_record = {}
    # needs to add author ID
    mong_record['Author'] = data['Author']
    mong_record['FILE_ID'] = data['File_ID']
    db_con = mongo_operation.get_db_conn()
    status = mongo_operation.delete_record(mong_record, db_con)
    logging.debug(status)
    return flask.jsonify(json.dumps({"FILE_ID":mong_record['FILE_ID'], "status": "deleted"}))

      
if __name__ == '__main__':
    api.run(host="0.0.0.0", port=6116, debug=True)

