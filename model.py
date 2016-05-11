"""Models and database functions for Rides project"""

from flask_sqlalchemy import SQLAlchemy
import correlation

#This is the connection to the PostgreSQL database; I'm getting this through
# the Flask-SQLAlchemy helper library. On this, we can find 'session'
# object, where I'm doing most of the interactions (like commiting, creating
# relationships etc.)

db = SQLAlchemy()

#############################################################################
# Model definitions
# Part 1: Compose ORM

class User(db.Model):
    """Users (both passengers and drivers) of Scuber website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(50), nullable=True)

    #define relationship to the driver
    driver = db.relationship("Driver", backref="rides")

    #define relationship to the passenger
    passenger = db.relationship("Passenger", backref="rides")


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)

##############################################################################################
# This passenger is the user

class Ride(db.Model):
    """Scooter Rides"""

    __tablename__ = "rides"

    ride_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.driver_id'), nullable=True)
    passenger_id = db.Column(db.Integer, db.ForeignKey('driver.passenger_id'), nullable=True)
    passenger_location = db.Column(db.String(100), nullable=False)
    passenger_destination = db.Column(db.String(100), nullable=False)
    pick_up_time = db.Column(db.DateTime, nullable=True)

    #define relationship to the driver
    driver = db.relationship("Driver", backref="rides")

    #define relationship to the passenger
    passenger = db.relationship("Passenger", backref="rides")


    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Ride driver_id=%s passenger_id=%s passenger_location=%s passenger_destination=%s>"
                                                            % (self.driver_id,
                                                                self.passenger_id,
                                                                self.passenger_location,
                                                                self.passenger_destination))

##############################################################################################
# This passenger is the user

class Passenger(db.Model):
    """Passengers who are taking scooter rides"""

    __tablename__ = "passengers"


    passenger_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    firstname = db.Column(db.String(30), nullable=True)
    lastname = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Passenger passenger_id=%s firstname=%s lastname=%s email=%s password=%s>"
                                                            % (self.passenger_id,
                                                                self.firstname,
                                                                self.lastname))

##############################################################################################
# This driver is the second user
class Driver(db.Model):
    """Drivers who are accepting passengers for scooter rides"""

    __tablename__ = "drivers"


    driver_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    firstname = db.Column(db.String(30), nullable=True)
    lastname = db.Column(db.String(30), nullable=False)
    driver_location = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Driver driver_id=%s firstname=%s lastname=%s driver_location%s>"
                                                            % (self.driver_id,
                                                                self.firstname,
                                                                self.lastname,
                                                                self.driver_location))

############################################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///rides'
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if I run this module interactively, it will leave
    # me in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
