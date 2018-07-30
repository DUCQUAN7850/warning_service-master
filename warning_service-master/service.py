# SIMPLE SERVICE 
from flask import Flask, request, json
from os import listdir, mkdir
from os.path import isdir, isfile, join
from shutil import rmtree
from datetime import datetime, timedelta
from database import DataBase
from warning import Warning
from anomaly_domain import AnomalyDomain
from start_all import sum
app = Flask(__name__)

app.config.update(SEND_FILE_MAX_AGE_DEFAULT=50)

host = "192.168.23.185"
db = DataBase(database="anomaly", collection="data", host=host)
warning = Warning(host=host)






# CONSTANT
##
MSG = {
        "SUCCESSFUL" : {"code":1, "msg" : "succesful"},
        "EXIST_TRUE" : {"code":0, "msg":"Repo is exist"},
        "EXIST_FALSE" : {"code":0, "msg":"Repo is not exist"},
        "WRONG_PASSWD": {"code":0, "msg":"wrong password"},
        "AUTHEN" :{"code":0, "msg":"repo is not exist or wrong password"},
        "WRONG_DATE" : {"code":0, "msg":"The datetime format s wrong"},
        "UPDATED" : {"code":0, "msg":"Value have been updated, please check lastest update"},
        "VALUE_FORMAT" : {"code":0, "msg":"Wrong value format (not enough values for 24h or value is not real"}
    }



###     FUNCTIONS 

# JSON response convert
def json_response (data) :
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response






####        ROUTING FUNCTIONS

# Create a new Repo. Data will be save into the STORAGE_FOLDER
@app.route("/create", methods=['POST'])
def create() :
    repo_name = request.form['name']
    repo_passwd = request.form['passwd']
    result = db.create_repo(name=repo_name, passwd=repo_passwd)
    warning.add_repo(name=repo_name)
    
    return json_response(result)
#==============================================================


# ===== Remove a existing repo from STORAGE_FOLDER =======
@app.route("/remove", methods=['POST'])
def remove() :
    repo_name = request.form['name']
    repo_passwd = request.form['passwd']
    warning.remove_repo(name=repo_name)

    return json_response(db.remove_repo(name=repo_name, passwd=repo_passwd))
#===========================================================


# ========== Update data by day ============================
@app.route("/update-by-day", methods=['POST'])
def update_by_day() :
    #-- inner function --
    def validate(date) :
        try :
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError :
            return False
        return True
    def get_last_update (name) :
        date = db.get_last_update(name=name)
        if date == '' : return date
        return datetime.strptime(date.split()[0], "%Y-%m-%d")

    #-------------
    repo_name = request.form['name']
    repo_passwd = request.form['passwd']
    date = request.form['date']
    value = request.form.getlist('value')
    
    if not validate(date) :
        return json_response (MSG["WRONG_DATE"])
    # check authen
    authen = db.check_authen(name=repo_name, passwd=repo_passwd)
    if authen != 1 :
        return json_response(authen) # authen is err msg 
    # check last update
    last_update = get_last_update(repo_name)
    if last_update != '' :
        if datetime.strptime(date, "%Y-%m-%d") <= last_update :
            return json_response( MSG["UPDATED"])
    # check value type
    if len(value) != 24 or any([not x.isdigit() for x in value]) :
        return json_response(MSG["VALUE_FORMAT"])
    
    else :
        return json_response(db.insert_date(name=repo_name, passwd=repo_passwd, date=date, value=value))
        
#==========================   



#=========    Update data by hour  ==============
@app.route("/update-by-hour", methods=['POST'])
def update_by_hour () :
    #-- inner function --
    def validate(date) :
        try :
            datetime.strptime(date, "%Y-%m-%d %H")
        except ValueError :
            return False
        return True
    
    def get_last_update(name) :
        date = db.get_last_update(name=name)
        if date == '' : return date
        return datetime.strptime(date, "%Y-%m-%d %H")

    def get_date (date) :
        return datetime.strptime(datetime.strftime(date, '%Y-%m-%d'), '%Y-%m-%d')
    
    #-------------------
    repo_name = request.form['name']
    repo_passwd = request.form['passwd']
    date = request.form['date']
    value = request.form['value']
    
    if not validate(date) :
        return json_response (MSG["WRONG_DATE"])
    #check authen
    authen = db.check_authen(name=repo_name, passwd=repo_passwd)
    if authen != 1 :
        return json_response(authen) # authen is err msg 
    #check last update
    last_update = get_last_update(repo_name)
    if last_update != '' :
        if datetime.strptime(date, "%Y-%m-%d %H") <= last_update :
            return json_response( MSG["UPDATED"])
    # check value type/format
    if not value.isdigit() :
        return json_response(MSG["VALUE_FORMAT"])
    
    else :
       return json_response(db.insert_hour(name=repo_name, passwd=repo_passwd, date=date, value=value)) 
        
    

### --  VISUALIZE DATA --
@app.route("/get-list-repo", methods=['POST'])
def get_list_repo () :
    list_repo = db.get_list_repo()
    return json_response(list_repo)



@app.route("/get-warning-data", methods=['POST'])
def get_warning_data () :
    repo_name = request.form['name']
    if db.get_last_update(name=repo_name) == '' :
        result = {"old":[], "current":[], "anomaly":[]}
        return json_response(data=result)
    # ---------------------------------------------------
    last_update =db.get_last_update(name=repo_name)
    if last_update == '' or not last_update:
        return "không tìm thấy last_update"
    else :
        last_update = datetime.strptime(last_update, "%Y-%m-%d %H")
    # --------------------------------------------------------
    # last_update = datetime.strptime(db.get_last_update(name=repo_name), "%Y-%m-%d %H")
    old_data = []
    for i in range(3) :
        date = datetime.strftime(last_update-timedelta(days=i), "%Y-%m-%d")
        old_data.append(db.get_data_by_day(name=repo_name, date=date))
    
    current = db.get_data_by_day(name=repo_name, date=datetime.strftime(last_update, "%Y-%m-%d"))
    
    anomaly = []
    for i in range(len(current)) :
        date = datetime.strftime(last_update, "%Y-%m-%d") + " " + str(i)
        warning_level = db.get_result(name=repo_name, date=date)
        if warning_level != None :
            if warning_level > 0 :
                anomaly.append(i)
    result = {"old":old_data, "current":current, "anomaly":anomaly}
    return json_response(data=result)
    

@app.route("/get-specific-data", methods=['POST'])
def get_specific_data () :
    def validate(date) :
        try :
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError :
            return False
        return True
        
    repo_name = request.form['name']
    date = request.form['date']
    if not validate(date) :
        return "wrong date format"

    # old data
    old_data = db.get_data_by_day(name=repo_name, date=date)
    old_status = []
    for i in range(len(old_data)) :
        warning_level = db.get_result(name=repo_name, date=date + ' ' + str(i))
        old_status.append(warning_level)
    old = [old_data, old_status]

    # curretn data
    last_update = datetime.strftime(datetime.strptime(db.get_last_update(name=repo_name), "%Y-%m-%d %H"), "%Y-%m-%d")
    current_data = db.get_data_by_day(name=repo_name, date=last_update)
    current_status = []
    for i in range(len(current_data)) :
        warning_level = db.get_result(name=repo_name, date=last_update + ' ' + str(i))
        current_status.append(warning_level)
    current = [current_data, current_status]

    result = {"old":old, "current":current}

    return json_response(result)


# chạy lại process khi đc gọi, biến truyền vào là tên repo
@app.route("/restart", methods=['POST'])
def restart() :
    name = request.form['name']
    new_process = AnomalyDomain(name=name, host=host)
    list_repo=db.get_list_repo()
    if name not in list_repo:
        return "Error!"
    else :
        return new_process.run()


#khởi động lại tất cả các process khi bật service
@app.route("/restart-all", methods=['POST'])
def restart_all() :
    list_repo = db.get_list_repo()
    l=[]
    for i in range(len(list_repo)):
        e = sum(list_repo[i])
        l.append(e)
    for i in range(len(list_repo)):
        l[i].start()
    for i in range(len(list_repo)):
        l[i].join()
#===========================
if __name__ == "__main__":
    app.run( port=8000, host="0.0.0.0", threaded=True, debug=True) #debug=True, use_reloader=True,