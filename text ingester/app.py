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


@api.route('/api/v1/textIngester',methods=['POST'])
def get_sentiment():
    
    try:
        json_of_metadatas = request.form.to_dict(flat=False)
        data = json_of_metadatas['data'][0]
        data = json.loads(data)
        
        
    except Exception as exp:
        logging.error("Got error in feteching json data {}".format(str(exp)))
    
    path, filename = util.save_file(request)
    logging.info("File name is {}".format(filename))
    text = util.extract_text_from_pdf(path)
    sentiment = util.get_sentiment(text)['results']
    
    mong_record = {}
    
    
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
    
        
if __name__ == '__main__':
    api.run(host="0.0.0.0", port=7117, debug=True)

