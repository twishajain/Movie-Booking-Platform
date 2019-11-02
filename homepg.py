from flask import Blueprint,request,render_template
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os
from datetime import date,time
import pymongo
from flask import jsonify, request
from flask_pymongo import PyMongo
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.mymongodb
registered_users = db.registered
movies= db.movies
hpg=Blueprint("hpg","hpg")

@hpg.route("/homepg", methods=['GET','POST'])
def homepg():
    email=request.values.get("email")
    psw=request.values.get("psw")
    if (email=='admin@gmail.com' and psw=="admin@gmail.com"):
        today = date.today()
        tdate = str(today.strftime("%Y-%m-%d"))
        print(tdate)
        return render_template("admin.html",date=tdate)
    if (email!=None):
        for r in registered_users.find():
            if (r["email"]==email and r["psw"]==psw):
                c=[]
                info={} 
                l=0
                for r in movies.find():
                    l=l+1
                    info['movie']=r['movie']
                    info['actor']=r['actor']
                    info['actress']=r['actress']
                    info['language']=r['language']
                    info['description']=r['description']
                    info['director']=r['director']
                    info['imageurl']=r['imageurl']
                    info['timeslot']=r['timeslot']
                    info['fromdate']=r['fromdate']
                    info['todate']=r['todate']
                    info['genre']=r['genre']
                    c.append(info)
                return render_template("landing.html",c=c,l=l)
        return render_template("error.html")
    return render_template("homepg.html")