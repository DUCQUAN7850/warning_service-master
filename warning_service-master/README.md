# Warning Moniter 
-------------------


----------------------

## Userage

Steps :
- Create your repo of data with a name and password 
- Add data to repo by day (24h) or by hour 
- See your result in user interface


### list response 
response message when status code = 200 (request succesful)
```
    "SUCCESSFUL" : {"code":1, "msg" : "succesful"},
    "EXIST_TRUE" : {"code":0, "msg":"Repo is exist"},
    "EXIST_FALSE" : {"code":0, "msg":"Repo is not exist"},
    "WRONG_PASSWD": {"code":0, "msg":"wrong password"},
    "AUTHEN" :{"code":0, "msg":"repo is not exist or wrong password"},
    "WRONG_DATE" : {"code":0, "msg":"The datetime format s wrong"},
    "UPDATED" : {"code":0, "msg":"Value have been updated, please check lastest update"},
    "VALUE_FORMAT" : {"code":0, "msg":"Wrong value format (not enough values for 24h or value is not real"}
```

------
## Create new data

**Describle** : create new data repo to get anomaly warning 

**URL** : `/create`

**Method** : `POST`

**Params** : 
```javascript
{ "name": "data-repo-name"}
```




--------

## Remove a data repo

**Describle** : remove a data repo 

**URL** : `/remove`

**Method** : `POST`

**Params** : 
```javascript
{ "name": "data-repo-name"}
```


--------------------------

## Update data by day

**Describle** : Add data to repo by day. <br>
(Warning: Cant Add data from day which is later than the day in last update. And the missing value is auto filled by zero) 

**URL** : `/update-by-day`

**Method** : `POST`

**Params** : 
```javascript
{ 
    "name"  : "data-repo-name",
    "date"  : "%Y-%m-%d",
    "value" : [0,1,2,...] (24 Real values)
}
```


------------------------------
## Update data by hour

**Describle** : Add data to repo by hour. <br>

**URL** : `/update-by-hour`

**Method** : `POST`

**Params** : 
```javascript
{ 
    "name"  : "data-repo-name",
    "date"  : "%Y-%m-%d %h",
    "value" : Real-Value
}
```



--------------------------
## Get warning status

```
pending this API for visualize 
```
**Describle** : Get warning status at a specific date

**URL** : `/get-warning`

**Method** : `POST`

**Params** : 
```javascript
{
     "name": "data-repo-name",
     "date": "%Y-%m-%d %h"
}
```

---------------------------

## -- Visualize API --

## Get list repo

**URL** : `/get-list-repo`

**Method** : `POST`

**Response example** : 
```javascript
["data 1", "data 2", "data 3"]
```

## Get warning data

**URL** : `/get-warning-data`

**Method** : `POST`

**Param** :
```javascript
{
    name : "data 1"
}
```

**Response example** : 
```javascript
{
    "old" : [ array1, array2 ],  
    // array1 and array2 is a array which had length = 24
    
    "current" : array3,  
    // array3 is an array which has length < 24 (not fixed size)

    "anomaly" : [0,1,10]
    // index of anomaly points 
}
```


## Get specific data

**URL** : `/get-specific-data`

**Method** : `POST`

**Param** :
```javascript
{
    name : "data 1",
    date : "%Y-%m-%d"
}
```

**Response example** : 
```javascript
{
   old : [data, status]
   current : [data, status]
   // Ex :
   // data :  [100,150,100,100,120,100,100]
   // status :[0,  1,  0,  0,  2,   0,  0]
}
```


## Restart process

**URL** : `/restart`

**Method** : `POST`


## Restart all

**URL** : `/restart-all`

**Method** : `POST`