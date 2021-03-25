
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

def search(data, client_db):
    
    mycol = client_db["authors"]
    mydoc = mycol.find(data)
    count = 0
    for x in mydoc:
        count += 1
    return count


def full_text_search(data, client_db):
    
    mycol = client_db["textmaintainer"]
    text = data['keyword']
    res = mycol.find({"$text": {"$search": text}})
    logging.info("Result count is {}".format(res.count()))
    logging.info("Type is {}".format(type(res)))
    file_id = list()
    access = list()
    
    for x in res:
        file_id.append(x['FILE_ID'])
        #logging.debug("Aythor:{}, ID:{}".format(x['AuthorID'],x['Author']))
        if x.get('AuthorID', None)  == data['AuthorID']:
            access.append(1)
        else:
            access.append(0)
    return file_id, access

   
def search_on_id(data, client_db):
    
    mycol = client_db["textmaintainer"]
    query = {"FILE_ID":data['FILE_ID']}
    
    out = mycol.find(query)
    for val in out:
        logging.info("Out:{}".format(val))
        content = val['content metadata']
    return content

def insert_record(data, client_db):
    
    mycol = client_db["textmaintainer"]
    x = mycol.insert_one(data)
    return x

def update_record(data, client_db):
    
    mycol = client_db["textmaintainer"]
    #count = search(data, client_db)
    #if count == 1:
    myquery = { "Author":data['Author'], "FILE_ID":data["FILE_ID"]}
    
    newvalues = { "$set": data }
    result = mycol.update_one(myquery, newvalues)
    return result

def  delete_record(data, mg_client):
    
    mycol = mg_client["textmaintainer"]
    myquery = data
    logging.debug(myquery)
    result = mycol.delete_one(myquery)
    
    # print the API call's results
    logging.debug("API call recieved:".format(result.acknowledged))
    logging.debug("Documents deleted:".format(result.deleted_count))
    return result

def  register(data, mg_client):
    """
    registering  user
    """
    mycol = mg_client["authors"]
    x = mycol.insert_one(data)
    return x

    
