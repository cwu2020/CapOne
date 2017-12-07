We wanted there to be a user portal for the website, so the home page is the login page where users can login or choose to create an account.
The background color is sky blue because of an HTML setting, and the Cap One -- an airbnb helper logo was created on a website, where we entered the information we wanted
and then chose a format and downloaded a png file. The login portal was created using a lot of the same code from the finance pset. In application.py, the
def login() function is what logs a user in and ensures that they enter a username and passcode. Using, session["user_id"] = rows[0]["id"], we remember which user has logged in.
After logging in, users are redirected to the maps page.

If they haven't already created an account, they can click the register link, which will redirect them to the register page via /register.
Once on the register page, their entries for username and passcode will be saved to the capone.db users table. Both their username and password (as a hash) are saved.
This code is also written based off of pset7 finance, where we created a registration page for new users. After registering, the user is redirected to the maps page. That is, they
are automatically logged in.

The map was taken largely from pset 8, although the markers are now based on a csv file of airbnb listings in San Fransisco (a city with a critical mass of airbnb listings).
Like in Mashup, more listings will pop up if you zoon in closer. We changed the search box to be a latitude/longitude search, since it would allow for the greatest freedom for the user.
For example, if the user hasn't built the property yet, or if the property is unlisted in Google Places, the user can still search for their property and get an optimal price point
at that location. Currently, the optimal price point takes all the existing properties within an approximate 1km radius and finds the most successful two properties and looks at their
price points to determine how the user should price their property. It finds the weekly average in that area by taking the weekly averages (based on number of bookings a week) of
every property and averaging them.

The graphs were done by using the Google Charts API and uploading JSONified data to each axis.

