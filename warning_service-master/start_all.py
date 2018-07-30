import threading
from anomaly_domain import AnomalyDomain
from database import DataBase



host = "192.168.23.185"
db = DataBase(database="anomaly", collection="data", host=host)



class sum(threading.Thread):
    def __init__(self,name):
        super(sum, self).__init__()
        self.name=name
    def run(self):
        self.new_process = AnomalyDomain(name=self.name, host=host)
        self.new_process.run()

# list_repo = db.get_list_repo()
# l=[]
# for i in range(len(list_repo)):
#     e = sum(list_repo[i])
#     l.append(e)
# for i in range(len(list_repo)):
#     l[i].start()
# for i in range(len(list_repo)):
#     l[i].join()