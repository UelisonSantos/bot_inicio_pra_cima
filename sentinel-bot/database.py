DB_URI = "mongodb://admin:senh4fort3!#@mongo:27017"

from pymongo import MongoClient

def insert_alarm(alarmdict):
    client = MongoClient(DB_URI)
    client.data.alarms.insert_one(alarmdict)
    client.close()
    return True

def get_all_alarms():
    client = MongoClient(DB_URI)
    result = client.data.alarms.find()
    client.close()
    return result

def get_alarms(chat_id, stock=None):
    client = MongoClient(DB_URI)
    result = None
    query = None    
    if stock is None:
        query = {"chat_id": str(chat_id)}
        
    else:
        query = {"chat_id": str(chat_id), "stock": str(stock)}
    result = client.data.alarms.find(query)
    client.close()
    return result

def delete_alarms(chat_id, stock=None):
    client = MongoClient(DB_URI)
    result = None
    query = None
    if stock is None:
        query = {"chat_id": str(chat_id)}
    else:
        query = {"chat_id": str(chat_id), "stock": str(stock)}
    result = client.data.alarms.delete_many(query)    
    client.close()
    return result