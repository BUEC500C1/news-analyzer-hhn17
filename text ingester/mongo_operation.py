
import config
import pymongo
import logging
from bson.objectid import ObjectId

def get_db_conn():
    
    try:
        myclient = pymongo.MongoClient(config.monog_address)
    except Exception as exp:
        logging.error("Failed to get connection, {}".format(str(exp)))
        
    mydb = myclient[config.db_name]
    return mydb

def insert_record(data, client_db):
    
    mycol = client_db["textmaintainer"]
    x = mycol.insert_one(data)
    return x

