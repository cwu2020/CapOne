import os
import re
import jinja2
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users

from flask import Flask, jsonify, render_template, request

from cs50 import SQL
from helpers import apology

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db2 = SQL("sqlite:///capone.db")

#from google.appengine.api import users - for Gmail login
env=jinja2.Environment(loader=jinja2.FileSystemLoader(''))

# This function creates a login for the user.  It will be displayed on every page
@app.route("/")
def gmail_login(self):
    user = users.get_current_user()
    if user:
                greeting = ('<a id = "greeting" >Welcome, %s!</a>' % user.nickname()+ ' ' + '<a href="%s">(sign out)</a>' %
                      users.create_logout_url('/'))
    else:
                greeting = ('<a href="%s">Sign in with a Google account</a>' %
                    users.create_login_url('/'))
    self.response.write('<html><body>%s</body></html>' % greeting)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Render map"""
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("index.html", key=os.environ.get("API_KEY"))



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

        # Redirect user to home page
        return jsonify(rows)



    # return jsonify(db.execute("SELECT * FROM listings WHERE latitude LIKE :q AND LONGITUDE LIKE :q2", q=q, q2=))
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
