Once logged onto the CS50 IDE, open a new terminal in the workspace. After opening a new terminal, move into the directory in which the project is located.
On my computer, the project is located in a cap-one-2 folder. In the terminal, I would enter: cd cap-one-2. To run it locally, I'd then enter in flask run. Now, on a separate page,
I can run my webpage. The link should be: http://ide50-kvaskas.cs50.io:8080/. This will take you to the home page of the website, where you should see a logo that says,
"Cap One - an Airbnb Helper" the background is a sky blue, and there is a login portal. If you do not already have a username and password combination, you can register by clicking
on the link that says: Don't Have an Account? Click to Register. The registration page has a boxes where you can insert a username you want and password. Once
you register, the page will automatically redirect you to the maps page.

Once on the maps page, you should see a format that says:  Welcome, {{ username }} (logout) at the top right. If you click this, it will take you back to the login
page of the website, logging you out. Underneath the welcome, the site asks you to enter the coordinates of your property. As an example, we've pre-entered the coordinates
37.7541839478958 for latitude and -122.406513787399 for longitude. After pressing submit, you should see a house icon pop-up where the location of your property is. Above the house pop-up will be a message.
At these particular coordinates, the message reads: The average weekly revenue is $56.161935482313666. You can maximize revenue at a price per night of $575.00. In general (for any coordinates entered), the message will let you know
the average weekly revenue for the airbnb listings in the neighborhood that you are looking at. It will also tell you how you can maximize your profit based on this data. Under the submit button on the left side there reads "Entry History". This link takes you to a user history page where you can see a history of all the latitude and
longitude coordinates previously entered. On the history page, there will be a link directing you back to the map page. This will read: Go Back To Map.

Before entering coordinates, you should see the map of San Fransisco with red logos that show listings in neighborhood areas, their cost, and how many people they can accomodate.
On the right side of the page are graphs representing San Fransisco by the numbers. These two graphs focus on the Castro neighborhood, where young tenants may be more price conscious
and responsive to crowd-sourced feedback. In the first graph, we see slightly more bookings at lower price points, and in the second graph, we see more upward spread in bookings as
the ratings move toward 100. The neighborhood with the best reviews is Presidio, with an average score of 97.6666667. For confirmation, check out the JSON data here:
http://personal-carrawu1.cs50.io:8080/bestneighborhood.


Ultimately, the functioanlity of the website is to allow you to enter your longitude and latitude, click submit, and you see a little gray house pop up on your map. Based on the
surrounding Airbnb listings, a little text box should appear that has information about weekly revenue and optimal price points. The side bar is for data visualizations and extras.
