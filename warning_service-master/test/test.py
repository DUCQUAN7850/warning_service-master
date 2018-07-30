# from datetime import datetime

# string = "2014-02-02 04"

# x = datetime.strptime( string,"%Y-%m-%d %H")

# print(x)




#===============================================
from pymongo import MongoClient
from database import DataBase

client = MongoClient('localhost', 27017)
db = client['anomaly']
collection = db['data']
from pprint import pprint
cursor = collection.find({})
for document in cursor: 
    pprint(document["name"])
    pprint(document["result"])

# db = DataBase(database="anomaly", collection="data")
# print(db.get_list_repo())





# cursor = collection.find({"name":"name-1" ,"data.2015-12-02":{"$exists": True}})

def check_exist (key="", conditions=[]) :
    # key = key1.key2.key3...
    # condition : list condition like [("name":"Tung"), ("age":"12")]
    exist_query = {}
    if key != "" :
        exist_query[key] = {"$exists":True}
    for key, value in conditions :
        exist_query[key] = value
    result = collection.find(exist_query)
    return result

# cursor = check_exist(key="data.2017-12-02",conditions=[("name","data")])
# existed = True if cursor.count() != 0 else False
# if existed :
#     document = cursor.next()
#     print ("document :::", document["data"]["2017-12-02"])
# print (cursor.count())


# for document in cursor: 
#     pprint(document)
#     # mongo_id = document["_id"]
#     # collection.update_one({'_id':mongo_id}, {"$set": {"data.2015-12-02": [1,2,3,4]}}, upsert=False)

