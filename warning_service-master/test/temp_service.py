from flask import Flask, request, json
# import matplotlib.pyplot as plt
from random import randint
from datetime import datetime

app = Flask(__name__)

app.config.update(SEND_FILE_MAX_AGE_DEFAULT=10)

x = [1791,961,584,469,567,915,2257,3699,5334,6532,7149,6738,7011,7095,6898,5961,4993,3886,4668,5222,6585,6777,5747,3800]


@app.route('/get-list-repo', methods=['GET', 'POST'])
def summary():  
    data = ["data_1", "data_2", "data_3"]
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/get-warning-data', methods=['GET','POST'])
def get_warning_data():
    old = []
    for i in range(3) :
        x1 = [e+randint(100,600)  for e in x]
        old.append(x1)
    
    data = {}
    data["old"] = old
    data["current"] = x[:20]
    data["anomaly"] = [0,1,10]

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/get-specific-data', methods=['GET','POST'])
def get_specific_data():
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

    data = [e+randint(100,600)  for e in x]
    status = [0 if i%7!=0 else 1 for i in range(24)]
    old = [data, status]

    data = [e+randint(100,600)  for e in x[:20]]
    status = [0 for i in range(24)]
    status[0] = 1
    status[1] = 3
    status[10] = 2
    current = [data, status]

    result = {}
    result["old"] = old
    result["current"] = [data, status]

    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response






if __name__ == "__main__":
    app.run( port=8080, host="0.0.0.0", threaded=True)






# for i in range(5) :
#     x = [e+randint(10,600)  for e in x1]
#     plt.plot(range(0,24), x, 'yo--')

# x = [e+randint(10,700)  for e in x1]
# plt.plot(range(0,20), x[:20], 'ko--')

# plt.plot(5, x[5], 'ro')
# plt.plot(10, x[10], 'ro')
# plt.plot(12, x[12], 'ro')

# plt.show()

