from flask import Flask, render_template,request,redirect,url_for # For flask implementation
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
theatres=db.theatres
bookings=db.bookings
app = Flask(__name__)
app.config['LAST']=""
app.config['CURRMOVIE']=""
app.config['CURRTHEATRE']=""
app.config['CURRUSER']=""
app.config['CURRSEATS']=[]
@app.route("/")
def home():
    app.config['LAST']="homepg.html"
    return render_template("homepg.html")
@app.route("/terms")
def terms():
    app.config['LAST']="terms.html"
    return render_template("terms.html")
@app.route("/booktickets")
def booktickets():
    timeslot=""
    minbooking=""
    maxbooking=""
    moviename=app.config['CURRMOVIE']
    print(moviename)
    for r in movies.find():
        if(r["movie"]==moviename):
            print(r["timeslot"])
            minbooking=r["fromdate"]
            maxbooking=r["todate"]
            timeslot=r["timeslot"]
    app.config['LAST']="booktickets.html"
    return render_template("booktickets.html",moviename=moviename,timeslot=timeslot,minbooking=minbooking,maxbooking=maxbooking)
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
    
    y=[]
    n=0
    for r in theatres.find():
        if(r["name"]==app.config['CURRTHEATRE']):
            y=r["filled"]
            n=r["num"]
    print("y:",y)
    sel_seats=request.values.get("seatlist")
    sel_seats=sel_seats.split("x")
    print (sel_seats)
    s=sel_seats[:]
    sel_seats=y+sel_seats
    numseats=request.values.get("numseats")
    theatres.remove({"name":app.config['CURRTHEATRE']})
    theatres.insert({"name":app.config['CURRTHEATRE'],"filled":sel_seats,"num":n})
    bookings.insert({"email":app.config['CURRUSER'],"movie":app.config['CURRMOVIE'],"seats":s})
    app.config['LAST']="payment.html"
    return render_template("payment.html",num=numseats)
@app.route("/seats", methods=['GET','POST'])
def seats():
    filled=[]
    num=0
    theatre=request.values.get("slct1")
    print(theatre)
    app.config['CURRTHEATRE']=theatre
    for r in theatres.find():
        if (r["name"]==theatre):
            filled=r["filled"]
            num=r["num"]
    app.config['LAST']="seats.html"
    return render_template("seats.html",filled=filled,n=num,theatre=theatre)
@app.route("/description/<moviename>", methods=['GET','POST'])
def description(moviename):
    app.config['LAST']="description.html"
    app.config['CURRMOVIE']=moviename
    for r in movies.find():
        if (r["movie"]==moviename):
            name=r["movie"]
            moviename=r["description"]
            actor=r["actor"]
            actress=r["actress"]
            director=r["director"]
            genre=r["genre"]
            lang=r["language"]
            imageurl=r["imageurl"]
            print(name)
    return render_template("description.html",name=name,moviename=moviename,actor=actor,actress=actress,director=director,genre=genre,lang=lang,imageurl=imageurl)
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
@app.route("/orders", methods=['GET','POST'])
def orders():
    return render_template("orders.html")
@app.route("/homepg", methods=['GET','POST'])
def homepg():
    email=request.values.get("email")
    psw=request.values.get("psw")
    if (email=='admin@gmail.com' and psw=="admin@gmail.com"):
        today = date.today()
        tdate = str(today.strftime("%Y-%m-%d"))
        print(tdate)
        return render_template("admin.html",date=tdate)
    if (email!=None):
        app.config['CURRUSER']=email
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
if __name__ == "__main__":
    app.run(debug=True)
