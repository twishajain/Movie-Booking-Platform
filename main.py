from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os
from datetime import date,time
import pymongo
from flask import jsonify, request
from flask_pymongo import PyMongo
from homepg import hpg
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.mymongodb
registered_users = db.registered
movies= db.movies
theatres=db.theatres
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
@app.route("/booktickets",  methods=['GET','POST'])
def booktickets():
    app.config['LAST']="booktickets.html"
    return render_template("booktickets.html")
@app.route("/landing", methods=['GET','POST'])
def landing():
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
    app.config['LAST']="landing.html"
    return render_template("landing.html",c=c,l=l)
app.register_blueprint(hpg)
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
@app.route("/payment", methods=['POST','GET'])
def payment():
    sel_seats=request.values.get("seatlist")
    sel_seats=sel_seats.split("x")
    print(sel_seats)
    theatres.remove({"name":"Bharath Cinemas"})
    theatres.insert({"name":"Bharath Cinemas","filled":sel_seats,"num":2})
    app.config['LAST']="payment.html"
    return render_template("payment.html")
@app.route("/seats", methods=['GET','POST'])
def seats():
    filled=[]
    for r in theatres.find():
        print(r["filled"])
        filled=r["filled"]
        num=r["num"]
    # print(filled)
    # for i in range(len(filled)):
    #     filled[i] = '_'.join([str(int(i)) for i in filled[i].split("_")])
    app.config['LAST']="seats.html"
    return render_template("seats.html",filled=filled,n=num)
@app.route("/description/<moviename>", methods=['GET','POST'])
def description(moviename):
    app.config['LAST']="description.html"
    for r in movies.find():
        if (r["movie"]==moviename):
            moviename=r["description"]
            actor=r["actor"]
            actress=r["actress"]
            director=r["director"]
            genre=r["genre"]
            lang=r["language"]
            imageurl=r["imageurl"]
    return render_template("description.html",moviename=moviename,actor=actor,actress=actress,director=director,genre=genre,lang=lang,imageurl=imageurl)
@app.route("/added", methods=['GET','POST'])
def added():
    movie=request.values.get("movie")
    actor=request.values.get("actor")
    actress=request.values.get("actress")
    director=request.values.get("director")
    language=request.values.get("language")
    description=request.values.get("description")
    fromdate=request.values.get("fromdate")
    todate=request.values.get("todate")
    timeslot=request.values.get("timeslot")
    genre=request.values.get("genre")
    imageurl=request.values.get("imageurl")
    movies.insert({ "movie":movie, "actor":actor, "actress":actress, "director":director, "language":language, "description":description, "imageurl":imageurl, "timeslot":timeslot, "fromdate":fromdate,"todate":todate, "genre": genre})
    app.config['LAST']="added.html"
    return render_template("added.html")
if __name__ == "__main__":
    app.run(debug=True)
