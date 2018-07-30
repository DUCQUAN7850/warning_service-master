from pymongo import MongoClient
from pprint import pprint

class DataBase :
    # MongoDB database connector class
    
    def __init__(self, host="localhost", port=27017, database="test", collection="test") :
        
        client = MongoClient(host, port)
        self.collection = client[database][collection]

        self.MSG = {
            "SUCCESSFUL" : {"code":1, "msg" : "succesful"},
            "EXIST_TRUE" : {"code":0, "msg":"Repo is exist"},
            "EXIST_FALSE" : {"code":0, "msg":"Repo is not exist"},
            "WRONG_PASSWD": {"code":0, "msg":"wrong password"}
        }
        return


    # --- PRIVATE FUNCTION -------------------------------------------------------------------------
    #    
    def __find_many (self, exist_key="", conditions=[]) :
        # key = key1.key2.key3...
        # condition : list tuples of conditions like [("name":"Tung"), ("age":"12")]
        # return a cursor of matching data
        exist_query = {}
        if exist_key != "" :
            exist_query[exist_key] = {"$exists":True}
        for key, value in conditions :
            exist_query[key] = value
        result = self.collection.find(exist_query)
        return result


    def __check_password (self, name="",passwd="") :
        # Check if matching password of a repo
        repo = self.__find_many (conditions=[("name",name)]).next()
        if passwd != repo["passwd"] :
            return False
        else : return True


    def __check_exist_repo (self, name="") : 
        # check if a repo name is exist
        repo_cursor = self.__find_many (conditions=[("name",name)])
        existed = True if repo_cursor.count() != 0 else False
        if existed : return True
        else : return False
    

    def __insert_date (self, name="", date="", value=[]) :
        # insert data by date (list : 24 elements)
        document = self.__find_many (conditions=[("name",name)]).next()
        mongo_id = document["_id"]
        data = "data." + date
        
        self.collection.update_one({'_id':mongo_id}, {"$set": {data: value}}, upsert=False)
        last_update = date + ' 23'
        self.collection.update_one({'_id':mongo_id}, {"$set": {"lastest": last_update}}, upsert=False)
        return


    def __insert_hour (self, name="", date="", value=0, hour=0) :
        #insert value for lastest hour (float)
        # insert into collection.data.date-time
        def get_list_value (hour=0, list_value=[], value=0) :
            # return values after update new value
            while len(list_value) <= hour :
                if len(list_value) == hour : list_value.append(value)
                else : list_value.append(0)
            return list_value

        document = self.__find_many (conditions=[("name",name)]).next()
        mongo_id = document["_id"]
        data = "data." + date
        repo_cursor = self.__find_many (exist_key=data, conditions=[("name", name)])
        existed = True if repo_cursor.count() != 0 else False
        
        if existed :
            new_value = get_list_value(hour=hour, list_value=document["data"][date], value=value)
            last_update = date + ' ' + str(hour)
            self.collection.update_one({'_id':mongo_id}, {"$set": {data: new_value}}, upsert=False)
            self.collection.update_one({'_id':mongo_id}, {"$set": {"lastest": last_update}}, upsert=False)
        else :
            new_value = get_list_value(hour=hour, list_value=[], value=value)
            last_update = date + ' ' + str(hour)
            self.collection.update_one({'_id':mongo_id}, {"$set": {data: new_value}}, upsert=False)
            self.collection.update_one({'_id':mongo_id}, {"$set": {"lastest": last_update}}, upsert=False)
        return

        
    def __insert_result (self, name="", date="", value=0) :
        document = self.__find_many (conditions=[("name",name)]).next()
        mongo_id = document["_id"]
        data = "result." + date
        self.collection.update_one({'_id':mongo_id}, {"$set": {data: value}}, upsert=False)
        return 

    
    def __check_repo_null (self, name="") :
        document = self.__find_many (conditions=[("name",name)]).next()
        start_date = document["start-date"]
        if start_date == "" :
            return True 
        else :
            return False

    def __setup_start_date (self, name="", date="") :
        document = self.__find_many (conditions=[("name",name)]).next()
        mongo_id = document["_id"]
        data = "start-date"
        date = date + " 0"
        self.collection.update_one({'_id':mongo_id}, {"$set": {data: date}}, upsert=False)
        return 


    # --- PUBLIC FUNCTION ---------------------------------------------------------------------------
    def check_authen (self, name="", passwd="") :
        # If OK return 1, else return error msg
        if self.__check_exist_repo(name=name) :
            if self.__check_password(name=name, passwd=passwd) :
                return 1 
            else : 
                return self.MSG["WRONG_PASSWD"]
        else :
            return self.MSG["EXIST_FALSE"]


    def create_repo (self, name="", passwd="") :
        existed = self.__check_exist_repo (name=name)
        if existed :
            return self.MSG["EXIST_TRUE"]
        else :
            new_repo = {
                "name" : name,
                "passwd" : passwd,
                "data" : {},
                "lastest" : "",
                "start-date" : "",
                "result" : {}
            }    
            self.collection.insert_one(new_repo)
            return self.MSG["SUCCESSFUL"]


    def remove_repo (self, name="", passwd="") :
        repo_cursor = self.__find_many (conditions=[("name",name)])
        existed = True if repo_cursor.count() != 0 else False
        if existed :
            repo = repo_cursor.next()
            if passwd != repo["passwd"] :
                return self.MSG["WRONG_PASSWD"]
            self.collection.remove(repo["_id"])
            return self.MSG["SUCCESSFUL"]
        else :
            return self.MSG["EXIST_FALSE"]


    def insert_date (self, name="", passwd="", date="",value=[]) :
        if not self.__check_exist_repo (name=name) :
            return self.MSG["EXIST_FALSE"]
        else :
            if not self.__check_password(name=name, passwd=passwd) :
                return self.MSG["WRONG_PASSWD"]
            
            # if every thing passed
            if self.__check_repo_null(name=name) :
                self.__setup_start_date (name=name, date=date)
            self.__insert_date (name=name, date=date, value=value)
            return self.MSG["SUCCESSFUL"]


    def insert_hour (self, name="", passwd="", date="", value=0) :
        if not self.__check_exist_repo (name=name) :
            return self.MSG["EXIST_FALSE"]
        else :
            if not self.__check_password(name=name, passwd=passwd) :
                return self.MSG["WRONG_PASSWD"]
            
            # if every thing passed
            if self.__check_repo_null(name=name) :
                self.__setup_start_date (name=name, date=date.split()[0])
            self.__insert_hour (name=name, date=date.split()[0], value=value, hour=int(date.split()[1]))
            return self.MSG["SUCCESSFUL"]


    def get_last_update (self, name="") :
        if not self.__check_exist_repo (name=name) :
            return False
        else :
            result = self.collection.find_one({"name":name})["lastest"]
            return '' if result == None else result


    def get_start_date (self, name="") :
        if not self.__check_exist_repo (name=name) :
            return False
        else :
            result = self.collection.find_one({"name":name})["start-date"]
            return '' if result == None else result


    def insert_result (self, name="", date="", value=0) :
            
            self.__insert_result (name=name, date=date, value=value)
            return self.MSG["SUCCESSFUL"]
    

    def get_result (self, name="", date="") :
        # get result of specific date from a repo 
        repo_cursor = self.__find_many (exist_key="result."+date, conditions=[("name",name)])
        existed = True if repo_cursor.count() != 0 else False
        if existed :
            document = repo_cursor.next()
            return document["result"][date]
        else :
            return None


    def get_data_by_hour (self, name="", date="", hour=0) :
        repo_cursor = self.__find_many (exist_key="data."+date, conditions=[("name",name)])
        existed = True if repo_cursor.count() != 0 else False
        if existed :
            document = repo_cursor.next()
            return document["data"][date][hour]
        else :
            return 0


    def get_data_by_day (self, name="", date="") :
        repo_cursor = self.__find_many (exist_key="data."+date, conditions=[("name",name)])
        existed = True if repo_cursor.count() != 0 else False
        if existed :
            document = repo_cursor.next()
            return document["data"][date]
        else :
            return [0 for i in range(24)]


    def get_list_repo (self) :
        repo_cursor = self.__find_many(exist_key="name")
        list_repo = [doc["name"] for doc in repo_cursor]
        return list_repo


#------------------------       end code   ------------------------------------------




#=============  test ==============================
# x = DataBase(database="anomaly", collection="data")
# print (x.delete_repo(name="new", passwd="1"))
# x.create_repo (name="data", passwd="1")
# a = [i for i in range(24)]
# x.insert_hour(name="data", passwd="1", date="2018-01-03 05", value=10)
# print (x.insert_hour(name="my_repo", passwd="1", date="2018-01-02", value=10))
# x.get_last_update(name="my_repo")
# print (x.get_result(name="data", date="2017-03-04 02"))
# print (x.get_data(name="my_repo", date="2018-02-18",hour=10))