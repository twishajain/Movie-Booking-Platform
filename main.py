from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os
import pymongo
from flask import jsonify, request
from flask_pymongo import PyMongo
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.mymongodb
registered_users = db.registered
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("homepg.html")
@app.route("/terms")
def terms():
    return render_template("terms.html")
@app.route("/homepg", methods=['GET','POST'])
def homepg():
    email=request.values.get("email")
    psw=request.values.get("psw")
    for r in registered_users.find():
        if (r["email"]==email and r["psw"]==psw):
            return render_template("homepg.html")
    return render_template("error.html")
@app.route("/regSuccess", methods=['GET','POST'])
def regSuccess():
    email=request.values.get("email")
    psw=request.values.get("psw")
    psw_repeat=request.values.get("psw_repeat")
    if (psw==psw_repeat):
        registered_users.insert({ "email":email, "psw":psw})
        return render_template("regSuccess.html")
    else:
        return render_template("error.html")
@app.route("/register")
def register():
    return render_template("register.html")
@app.route("/error")
def error():
    return render_template("error.html")
@app.route("/login")
def login():
    return render_template("login.html")
if __name__ == "__main__":
    app.run(debug=True)
