from anomaly_detection import Amean 
from multiprocessing import Process, Queue
from database import DataBase 
from datetime import datetime, timedelta  
import time 
import traceback


class AnomalyDomain (Process):
    # initilize data 
    def __init__(self, name, host) :
        super(AnomalyDomain, self).__init__()
        self.name = name
        self.db = DataBase(host=host, database="anomaly", collection="data")
        self.last_update = ""
        self.last_value = 0
        
        self.timeline = []
        for i in range(24) :
            hour_detection = Amean()
            self.timeline.append(hour_detection)
        
        self.timeline_weekend = []
        for i in range(24) :
            hour_detection = Amean()
            self.timeline_weekend.append(hour_detection)        
        return 

    def __predict (self, hour=0, current=0, angle=0, date="") :
        """predict and return value for new data point"""
        date = datetime.strptime(date, "%Y-%m-%d")
        code = self.timeline[hour].predict(current=current, angle=angle)
        if code == '' :
            return 10
        else :
            return code
            

    def __log (self, msg) :
        with open("log.txt","a") as f :
            f.write(msg + '\n')
        return 

    def __check_new_data (self, name) :
        """check if there is new data in repo
            if yes, return all new data"""
        # check if repo is null (start-date = null)
        if self.last_update == "" :
            start_date = self.db.get_start_date(name=name)
            if start_date != '' :
                self.last_update = start_date

        # check last update
        # go to database and get last_update, then update data in anomaly class (this class)
        db_last_update = self.db.get_last_update(name=name)
        print("db_last_update: ",db_last_update)
        if db_last_update == '' or not db_last_update:
            return []
        else :
            db_last_update = datetime.strptime(db_last_update, "%Y-%m-%d %H")  
        last_update = datetime.strptime(self.last_update,  "%Y-%m-%d %H")
        result = []
        while last_update < db_last_update :
            print("db_last_update: ", name," ", db_last_update)
            last_update += timedelta(seconds=3600)
            print("check last update :", last_update)
            date = last_update.strftime("%Y-%m-%d")
            hour = last_update.hour
            data_value = self.db.get_data_by_hour(name=name, date=date, hour=hour) 
            self.__log(date + ' ' + str(hour) + ' ' + str(data_value))
            data = {'angle':float(data_value)-float(self.last_value),
                    'current':data_value,
                    'date':date,
                    'hour':hour}
            result.append(data)
            self.last_value = data_value  
            
        self.last_update = datetime.strftime(last_update, '%Y-%m-%d %H')
        return result
        

    def __save_result (self, name, date, result) :
        self.db.insert_result(name=name, date=date, value=result)
        return 
        
    
    #=========================  RUN   ==============================    
    # Run process method
    # start per process by calling run()
    def run(self) :
        name = self.name     
        try :
            while True :
                time.sleep(10) 

                data = self.__check_new_data (name)
                # data :
                # [] : no new data
                # [ {date:, hour:, current:, angle:)]
                print("--------------AnomalyDomain is running1--------------")
                if data != [] :
                    print("--------------AnomalyDomain is running2--------------")
                    # predict new data
                    for hour_data in data :                
                        result_prediction = self.__predict(hour=hour_data['hour'], 
                                                           current=hour_data['current'], 
                                                           angle=hour_data['angle'],
                                                           date=hour_data["date"])
                        # save result to db
                        self.__save_result(name=name,
                                           date=hour_data['date']+' '+str(hour_data['hour']),
                                           result=result_prediction)
                
                #continue waiting 
        except Exception as e: 
            with open("log.txt","a") as f :
                f.write(str(e) + '\n')
                traceback.print_exc()