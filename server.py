"""Scuber Rides."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Driver, Ride, Passenger

from datetime import datetime


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

#making connection to homepage
@app.route('/')
def index():
    """Homepage."""

    #show me the register page

    return redirect("/register")


#making a connection to register
#getting the actual form
@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

#show mw the register_form.html
    return render_template("register_form.html")


#making a connection to register
@app.route('/register', methods=['POST'])
def register_process():
    """Process registration for passengers and drivers."""

    # Get form variables from register_form
    email = request.form.get("email")
    password = request.form.get("password")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")

    # we don't want to have 2 people checking in under same address
    print request.form['user_type']


    #adding new passenger and driver to the db
    if request.form["user_type"]=='passenger':
        # give me passenger with this email
        passenger = Passenger.query.filter_by(email=email).first()
        if passenger:
            flash("You have already registered as a passenger. Please log in.")
            return redirect('/login')
        new_passenger = Passenger(email=email, password=password, firstname=firstname, lastname=lastname)
        db.session.add(new_passenger)
        #committing the new driver and passenger to the db
        db.session.commit()
        #alert-message that will give name and email of passenger sign in
        flash("Passenger %s added." % email)
        # set passenger_id
        session["passenger_id"] = new_passenger.passenger_id
        return redirect("/feed")
    else:
        driver = Driver.query.filter_by(email=email).first()
        if driver:
            flash("You have already registered as a passenger. Please log in.")
            return redirect('/login')
        new_driver = Driver(email=email, password=password, firstname=firstname, lastname=lastname)
        db.session.add(new_driver)
        #committing the new driver and passenger to the db
        db.session.commit()
        #alert-message that will give name and email of driver sign in
        flash("Driver %s added." % email)
        #set driver_id
        session["driver_id"] = driver.driver_id
        return redirect("/feed")


#######################################################################################################
#Passenger and Driver login

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login passenger and driver."""

    #clears the session
    session.clear()

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    passenger_user = Passenger.query.filter_by(email=email).first()
    driver_user = Driver.query.filter_by(email=email).first()

    # please check if customers are registered users or not
    if not passenger_user and not driver_user:
    # if not alert message go to login
        flash("No such user. Please try again.")
        return redirect("/login")

    #if the user is a passenger
    if passenger_user:
        #and their password is correct
        if passenger_user.password == password:
            #using the session dictionary and registering the key and value
            session["passenger_id"] = passenger_user.passenger_id
            #go to the homepage
            return redirect("/feed")
        #if the user passengers password is incorrect
        else:
            #alert message that the password is incorrect
            flash("Incorrect password. Please try again.")
            #got to login page
            return redirect("/login")

    #if the user is not a passenger it's a driver
    if driver_user:
        #if the user driver enters in the correct password
        if driver_user.password == password:
            #using the session dictionary and registering the key and value
            session["driver_id"] = driver_user.driver_id
            #please direct them to the homepage
            return redirect("/feed")
        #if the user driver entered in an incorrect password
        else:
            #please alert message them that it was incorrect
            flash("Incorrect password")
            #and redirect them to the login page
            return redirect("/login")

@app.route('/logout')
def logout():
    """Log out."""

    #clears the session
    session.clear()
    flash("See you next time! You are logged out.")
    return redirect("/")


################################################################################################
# Feed page

@app.route('/feed', methods=['GET'])
def feed_list():
    """Show feed to passengers and drivers"""

    #list of objects
    all_rides = Ride.query.all()

    return render_template("feed.html", all_rides=all_rides)


##################################################################################################

@app.route('/rides', methods=['POST'])
def rides_list():
    """Show feed to passengers and drivers"""


    #getting information from form
    # firstname = request.form.get('firstname')
    # lastname = request.form.get('lastname')
    passenger_location = request.form.get('passenger_location')
    passenger_destination = request.form.get('passenger_destination')
    pick_up_time = request.form.get('pick_up_time')


    #if there is a passenger_id. Get the id.
    if 'passenger_id' in session:
        passenger_id = session['passenger_id']
        #creating row that has the passengers stored in database
        new_ride = Ride(passenger_location=passenger_location, passenger_destination=passenger_destination,
        pick_up_time=pick_up_time, passenger_id=passenger_id)

        db.session.add(new_ride)
        #db.session.flush()
        db.session.commit()
        to_return = str(new_ride.ride_id)
        return to_return # new_ride.to_json

    return "failed" #this line should never be reached
    #jsonify({"new_id": "new_ride.id"})
    #new_ride.id
    #jsonify({"dicts": "all_rides"})    " {"dicts": "all_rides"} "


###################################################################################################

###################################################################################################

# get this ride with this id <ride_id>
@app.route("/rides/<ride_id>", methods=['GET', 'POST'])
def update_ride(ride_id):
    """Rate passsenger and drivers"""

    # will get the ride id from the route. Example: Ride/1
    ride = Ride.query.get(ride_id)

    #getting the form
    if request.method == 'GET':
        return render_template("rating_form.html", ride=ride, session=session)
    else:
        passenger_rating = request.form.get('passenger_rating')
        driver_rating = request.form.get('driver_rating')

        #if passenger rating was in the form then set passenger rating
        #else if driver rating was in the form set driver rating
        #DOES NOT check if the user is a driver or a passenger
        if passenger_rating:
            ride.passenger_rating = passenger_rating
        elif driver_rating:
            ride.driver_rating = driver_rating

        db.session.commit()
        return redirect("/feed")


###################################################################################################
###################################################################################################
@app.route("/claim-rides/<ride_id>", methods=['POST'])
def claim_ride(ride_id):
    """Driver can claim passenger ride"""

    if 'passenger_id' in session:
        flash("You are not a driver.")
        return redirect("/feed")
    if 'driver_id' in session:
        # make new template for driver claim YAY
        ride = Ride.query #FIXME !
    return " THIS IS THE CLAIM RIDE PAGE :)"




#########################################################################################
# Debug

if __name__ == "__main__":
    app.debug = True
    # I am setting debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    # Do not debug for demo
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
