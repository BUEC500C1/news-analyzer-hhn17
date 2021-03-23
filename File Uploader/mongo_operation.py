
import config
import pymongo
import logging
from bson.objectid import ObjectId

def get_db_conn():
    """
    Fetch the mongodb connection 
    """
    try:
        myclient = pymongo.MongoClient(config.monog_address)
    except Exception as exp:
        logging.error("Failed to get connection, {}".format(str(exp)))
        
    mydb = myclient[config.db_name]
    return mydb

def search(data, client_db):
    """
    search function for mongodb client
    """
    mycol = client_db["textmaintainer"]
    myquery = {"_id": ObjectId('6039e735a535f959e38d1bda')}
    mydoc = mycol.find(myquery)
    count = 0
    for x in mydoc:
        count += 1
    return count
    
def insert_record(data, client_db):
    """
    inset record in mongodb database 
    """
    mycol = client_db["textmaintainer"]
    x = mycol.insert_one(data)
    return x

def update_record(data, client_db):
    """
    update the record with doc_id and
    
    """
    mycol = client_db["textmaintainer"]
    #count = search(data, client_db)
    #if count == 1:
    myquery = { "Author":data['Author'], "FILE_ID":data["FILE_ID"]}
    
    newvalues = { "$set": data }
    result = mycol.update_one(myquery, newvalues)
    return result

def  delete_record(data, mg_client):
    """
    delete record from database
    """
    mycol = mg_client["textmaintainer"]
    myquery = data
    logging.debug(myquery)
    result = mycol.delete_one(myquery)
    
    # print the API call's results
    logging.debug("API call recieved:".format(result.acknowledged))
    logging.debug("Documents deleted:".format(result.deleted_count))
    return result
