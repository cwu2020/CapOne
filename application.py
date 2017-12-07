import os
import re
import jinja2
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from datetime import datetime
from helpers import apology

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db2 = SQL("sqlite:///capone.db")

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Home page of website
@app.route("/", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db2.execute("SELECT * FROM users WHERE username =:username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Redirect user to index page
        return redirect("/index")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# site maps page
@app.route("/index")
def index():
    """Render map"""
    tablevalues = db2.execute(
    "SELECT username FROM users WHERE id=:id", id=session["user_id"])
    for tablevalue in tablevalues:
            name = tablevalue["username"]
    # allow us to welcome user by their username
    return render_template("index.html", username=name)

# registration page
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("missing username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("missing password", 400)

        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        # Query database for username
        hashpassword = generate_password_hash(request.form.get("password"))
        result = db2.execute("INSERT INTO users(username, hash) VALUES(:username, :hash)",
                            username=request.form.get("username"), hash=hashpassword)

        if not result:
            return apology("username already taken", 400)

        # Remember which user has logged in
        session["user_id"] = result

        # Redirect user to home page
        return redirect("/index")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/search", methods=['POST'])
def search():
    """Search for places that match query"""

    if request.method == "POST":
        # Ensure latitude was submitted
        if not request.form.get("lat"):
            return apology("please provide latitude and longitude", 403)

        # Ensure longitude was submitted
        elif not request.form.get("lng"):
            return apology("please provide longitude and longitude", 403)

        # rounds the entered coordinates to two decimal places, thus finding all the existing airbnb listings within a short distance (in the same neighborhood)
        lat= "{0:.2f}".format(float(request.form.get("lat"))) + "%"
        longi="{0:.2f}".format(float(request.form.get("lng"))) + "%"

        rows = db2.execute("SELECT price, reviews_per_month, latitude, longitude, neighbourhood_cleansed FROM listings WHERE latitude LIKE :lat AND longitude LIKE :longi", lat=lat, longi=longi)
         # store in history
        lati = request.form.get("lat")
        longit = request.form.get("lng")
        db2.execute("INSERT INTO userhistory (lat, longi, id) VALUES(:lat, :longi, :id)",
               lat=lati, longi=longit, id=session["user_id"])
        # Redirect user to home page
        return jsonify(rows)


@app.route("/bestneighborhood")
def bestneighborhood():
    rows = db2.execute("SELECT AVG(review_scores_rating), neighbourhood_cleansed FROM listings WHERE review_scores_rating NOT null AND review_scores_rating != '' GROUP BY neighbourhood_cleansed")
    return jsonify(rows)

@app.route("/otherdatapoints")
def otherdatapoints():
    rows = db2.execute("SELECT review_scores_rating, reviews_per_month FROM listings WHERE neighbourhood_cleansed LIKE 'Castro/Upper Market' AND review_scores_rating NOT null AND reviews_per_month !='' AND reviews_per_month != 223")
    return jsonify(rows)

@app.route("/datapoints")
def datapoints():
    rows = db2.execute("SELECT price, reviews_per_month FROM listings WHERE neighbourhood_cleansed LIKE 'Castro/Upper Market' AND price NOT null AND reviews_per_month !='' AND reviews_per_month != 223")
    return jsonify(rows)

@app.route("/update")
def update():
    """Find up to 10 places within view"""

    # Ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # Ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # Explode southwest corner into two variables
    sw_lat, sw_lng = map(float, request.args.get("sw").split(","))

    # Explode northeast corner into two variables
    ne_lat, ne_lng = map(float, request.args.get("ne").split(","))

    # Find 10 cities within view, pseudorandomly chosen if more within view
    if sw_lng <= ne_lng:

        # Doesn't cross the antimeridian
        rows = db2.execute("""SELECT * FROM listings
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
                          GROUP BY country_code, city, state""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # Crosses the antimeridian
        rows = db2.execute("""SELECT * FROM listings
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
                          GROUP BY country_code, city, state""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # Output places as JSON
    return jsonify(rows)

@app.route("/history")
def history():
    """Show history of coordinate entries"""
    allhistory = db2.execute("SELECT * from userhistory WHERE id=:id", id=session["user_id"])
    return render_template("history.html", userhistory=allhistory)