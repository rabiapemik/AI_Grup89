from db_creator import ignition, Base, engine, Session, users, patients, doktor, health_data, suggestions
from flask import Flask, render_template, request, redirect, url_for, session, redirect, send_file, flash

app = Flask(__name__)
app.secret_key = "secret_key"
#---------------------------------------------------------------------------------------------------------
#bu kod giriste default olarak ViteCheck-homepage.html sayfasinin render edilmesini saglar.
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("ViteCheck-homepage.html")
#---------------------------------------------------------------------------------------------------------
@app.route("/doktor-index", methods=["GET", "POST"])
def doktor_index():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

    #bu kod formdan gelen email ve sifre bilgilerinin databasedeki varligini kontrol eder.Ve uyan ilk kullaniciyi dondurur.
    user = users.query.filter_by(email=email, password=password).first()

    #buradaki kosullu ifade yukaridaki sorguda kullanici varsa ve sifre databasedeki sifre ile denk ise true doner. 
    if user and user.password == password:
        session["user_id"] = user.id
        return render_template("doctor_homepage.html")
    else:
        return render_template("doktor-index.html")
    
#---------------------------------------------------------------------------------------------------------

@app.route("/hasta-index", methods=["GET", "POST"])
def hasta_index():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

    #bu kod formdan gelen email ve sifre bilgilerinin databasedeki varligini kontrol eder.Ve uyan ilk kullaniciyi dondurur.
    user = users.query.filter_by(email=email, password=password).first()

    #buradaki kosullu ifade yukaridaki sorguda kullanici varsa ve sifre databasedeki sifre ile denk ise true doner. 
    if user and user.password == password:
        session["user_id"] = user.id
        return render_template("hasta_homepage.html")
    else:
        return render_template("hasta-index.html")
#---------------------------------------------------------------------------------------------------------