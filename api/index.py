from flask import Flask
from flask import Flask, flash, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_restful import Resource, Api
from flask import jsonify
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
import requests
import json
import time



obj = time.gmtime(0)
epoch = time.asctime(obj)
# print("The epoch is:",epoch)


# uri = "mongodb+srv://rpinformationhub:PFFS9HrqJ73Wnnhj@safe-drive.gwyfmpf.mongodb.net/?retryWrites=true&w=majority"
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

# mydb = client["news-api"]
# mycol = mydb["news-api"]

url = "https://newsapi.org/v2/everything"
# params = { 'a'
# requests.get(url, params={key: value}, timeout=5)

# mydict = { "name": "John", "address": "Highway 37" }

# x = mycol.insert_one(mydict)



app = Flask(__name__)


app.config['MONGODB_SETTINGS'] = {
    'host':'mongodb+srv://rpinformationhub:password@safe-drive.gwyfmpf.mongodb.net/?retryWrites=true&w=majority'
}



db = MongoEngine(app)


class News(db.Document):
    params = db.StringField(required=True)
    data = db.StringField(required=True)
    time = db.LongField(required=True)
   






@app.route('/', methods=['GET'])
def home():
    args = request.args
    print(args)
    params = {}
    curr_time = round(time.time())
    print("Milliseconds since epoch:",curr_time)


    for key in args:
        params[key] = args.get(key)
    print(params)
    params['apiKey'] = '48c829b7e4db4d0db9f0eea54e009a87'
    
    news = News.objects(params= str(params)).first()

    if(news != None and news.time!=None ):
     if (curr_time - news.time < 86400):
      print("sent from DB")
      return jsonify(json.loads(news.data)), 200

    # myquery = { "params": str(params) }

    # mydoc = mycol.find(myquery)
    # c=0
    # ret=''
    # for x in mydoc:
    #     c+=1
    #     ret = x['data']
    #     print(x)
    # if c== 0:
    res = requests.get(url, params=params)
    res = res.json()

    News.objects(params=params).delete()   
    movie = News(params= str(params), data= json.dumps(res),time= time.time()).save()
    print("sent from API")
    return res, 200
    
       
    

@app.route('/about')
def about():
    return 'About'
