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
movies= db.movies
app = Flask(__name__)
app.config['LAST']=""
@app.route("/")
def home():
    app.config['LAST']="homepg.html"
    return render_template("homepg.html")
@app.route("/terms")
def terms():
    app.config['LAST']="terms.html"
    return render_template("terms.html")
@app.route("/homepg", methods=['GET','POST'])
def homepg():
    email=request.values.get("email")
    psw=request.values.get("psw")
    if (email=="admin" and psw=="admin" and app.config['LAST']=="login.html"):
        app.config['LAST']="homepg.html"
        return render_template("admin.html")
    if (app.config['LAST']=="login.html"):
        for r in registered_users.find():
            if (r["email"]==email and r["psw"]==psw):
                app.config['LAST']="homepg.html"
                return render_template("homepg.html")
    if (app.config['LAST']=="login.html"):
        app.config['LAST']="homepg.html"
        return render_template("error.html")
    else:
        return render_template("homepg.html")
@app.route("/regSuccess", methods=['GET','POST'])
def regSuccess():
    email=request.values.get("email")
    psw=request.values.get("psw")
    psw_repeat=request.values.get("psw_repeat")
    if (psw==psw_repeat and len(psw)>=5):
        registered_users.insert({ "email":email, "psw":psw})
        app.config['LAST']="regSuccess.html"
        return render_template("regSuccess.html")
    else:
        app.config['LAST']="regSuccess.html"
        return render_template("error.html")
@app.route("/register")
def register():
    app.config['LAST']="register.html"
    return render_template("register.html")
@app.route("/error")
def error():
    app.config['LAST']="error.html"
    return render_template("error.html")
@app.route("/admin")
def admin():
    app.config['LAST']="admin.html"
    return render_template("admin.html")
@app.route("/login")
def login():
    app.config['LAST']="login.html"
    return render_template("login.html")
@app.route("/added", methods=['GET','POST'])
def added():
    movie=request.values.get("movie")
    actor=request.values.get("actor")
    actress=request.values.get("actress")
    director=request.values.get("director")
    language=request.values.get("language")
    description=request.values.get("description")
    imageurl=request.values.get("imageurl")
    movies.insert({ "movie":movie, "actor":actor, "actress":actress, "director":director, "language":language, "description":description, "imageurl":imageurl})
    app.config['LAST']="added.html"
    return render_template("added.html")
if __name__ == "__main__":
    app.run(debug=True)
