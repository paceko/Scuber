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
        passenger = Passenger.query.filter_by(email=email).one()
        #set passenger_id
        session["passenger_id"] = passenger.passenger_id
        return redirect("/feed")
    else:
        driver = Driver.query.filter_by(email=email).first()
        if driver:
            return redirect('/login')
        new_driver = Driver(email=email, password=password, firstname=firstname, lastname=lastname)
        db.session.add(new_driver)
        #committing the new driver and passenger to the db
        db.session.commit()
        #alert-message that will give name and email of driver sign in
        flash("Driver %s added." % email)
        driver = Driver.query.filter_by(email=email).one()
        #set driver_id
        session["driver_id"] = driver.driver_id
        return redirect("/drivers")


#######################################################################################################
#Passenger and Driver login

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login passenger and driver."""

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
            return redirect("/")
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
            return redirect("/")
        #if the user driver entered in an incorrect password
        else:
            #please alert message them that it was incorrect
            flash("Incorrect password")
            #and redirect them to the login page
            return redirect("/login")

@app.route('/logout')
def logout():
    """Log out."""

    del session["passenger_id"]
    flash("See you next time! You are logged out.")
    return redirect("/")


################################################################################################
# Feed page

@app.route('/feed', methods=['GET'])
def feed_list():
    """Show feed to passengers and drivers"""

    all_rides = Ride.query.all()

    return render_template("feed.html", all_rides=all_rides)


##################################################################################################

@app.route('/rides', methods=['POST', 'GET'])
def rides_list():
    """Show feed to passengers and drivers"""

    #getting information from form
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    passenger_location = request.form.get('passenger_location')
    passenger_destination = request.form.get('passenger_destination')
    pick_up_time = request.form.get('pick_up_time')


    #test if it's working
    print passenger_location
    print passenger_destination
    print pick_up_time


    #if there is a passenger_id. Get the id.
    if 'passenger_id' in session:
        passenger_id = session['passenger_id']
        #creating row that has the passengers stored in database
        new_ride = Ride(passenger_location=passenger_location, passenger_destination=passenger_destination,
        pick_up_time=pick_up_time, passenger_id=passenger_id)


        db.session.add(new_ride)
        db.session.commit()

        

        #  #testing with return text

        return jsonify({"dicts": "all_rides"})

    #if there is a driver_id. Get the id.
    # else:
    #     driver_id = session['driver_id']
    #     #creating row that has the drivers stored in database
    #     new_ride = Ride(driver_id=driver_id, passenger_location=passenger_location,
    #                     passenger_destination=passenger_destination, pick_up_time=pick_up_time,
    #                     pick_up_date=pick_up_date)



###################################################################################################
###################################################################################################
@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """Show info about user."""

    user = User.query.get(user_id)
    return render_template("user.html", user=user)


@app.route("/movies")
def movie_list():
    """Show list of movies."""

    movies = Movie.query.order_by('title').all()
    return render_template("movie_list.html", movies=movies)


@app.route("/movies/<int:movie_id>", methods=['GET'])
def movie_detail(movie_id):
    """Show info about movie.

    If a user is logged in, let them add/edit a rating.
    """
    print "made it here"

    movie = Movie.query.get(movie_id)

    user_id = session.get("user_id")

    if user_id:
        user_rating = Rating.query.filter_by(
            movie_id=movie_id, user_id=user_id).first()

    else:
        user_rating = None

    # Get average rating of movie

    rating_scores = [r.score for r in movie.ratings]
    avg_rating = float(sum(rating_scores)) / len(rating_scores)

    prediction = None

    # Prediction code: only predict if the user hasn't rated it.

    if (not user_rating) and user_id:
        user = User.query.get(user_id)
        if user:
            prediction = user.predict_rating(movie)

    # Either use the prediction or their real rating

    if prediction:
        # User hasn't scored; use our prediction if we made one
        effective_rating = prediction

    elif user_rating:
        # User has already scored for real; use that
        effective_rating = user_rating.score

    else:
        # User hasn't scored, and we couldn't get a prediction
        effective_rating = None

    # Get the eye's rating, either by predicting or using real rating

    the_eye = User.query.filter_by(email="the-eye@of-judgment.com").one()
    eye_rating = Rating.query.filter_by(
        user_id=the_eye.user_id, movie_id=movie.movie_id).first()

    if eye_rating is None:
        eye_rating = the_eye.predict_rating(movie)

    else:
        eye_rating = eye_rating.score

    if eye_rating and effective_rating:
        difference = abs(eye_rating - effective_rating)

    else:
        # We couldn't get an eye rating, so we'll skip difference
        difference = None

    # Depending on how different we are from the Eye, choose a message

    BERATEMENT_MESSAGES = [
        "I suppose you don't have such bad taste after all.",
        "I regret every decision that I've ever made that has brought me" +
            " to listen to your opinion.",
        "Words fail me, as your taste in movies has clearly failed you.",
        "Did you watch this movie in an alternate universe where your taste doesn't suck?",
        "Words cannot express the awfulness of your taste."
    ]

    if difference is not None:
        beratement = BERATEMENT_MESSAGES[int(difference)]

    else:
        beratement = None

    return render_template(
        "movie.html",
        movie=movie,
        user_rating=user_rating,
        average=avg_rating,
        prediction=prediction,
        eye_rating=eye_rating,
        difference=difference,
        beratement=beratement
        )


#########################################################################################
# Debug

if __name__ == "__main__":
    # I am setting debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
