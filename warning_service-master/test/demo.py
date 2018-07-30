import requests
from datetime import datetime, timedelta
from random import randint
import time


# DEMO SEND DATA

def get_data (f) :
        data = [int(x) for x in open("../view/"+f).read().split()]
        return data

# r = requests.post(url="http://localhost:8000/create", data={"name":"abc","passwd":"1"})
# print (r.status_code, r.text)

date = datetime.strptime("2016-05-25", "%Y-%m-%d")

for i in range(700) :

        date += timedelta(days=1)
        print("update data in: ", str(date))
        value = get_data(datetime.strftime(date, "%Y-%m-%d"))
        data = {"name":"db",
                "passwd":"1",
                "date":datetime.strftime(date, "%Y-%m-%d"),
                "value":value}

        r = requests.post(url = "http://localhost:8000/update-by-day", data = data)
        print (r.status_code, r.text)


for i in range(10) :
        date += timedelta(days=1)
        value = get_data(datetime.strftime(date, "%Y-%m-%d"))
        for i in range(len(value)) :
                data = {"name":"db",
                        "passwd":"1",
                        "date":datetime.strftime(date, "%Y-%m-%d") + ' ' + str(i),
                        "value":value[i]}
                r = requests.post(url = "http://localhost:8000/update-by-hour", data = data)

                time.sleep(10)
          
