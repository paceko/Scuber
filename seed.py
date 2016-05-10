from model import Ride, Passenger, Driver, connect_to_db, db
from server import app

"""Utility file to seed passengers (users)"""


#################################################################################
#Passengers (users)

passenger = Passenger(firstname='Harry',
                    lastname='Potter',
                    email='harry@gmail.com',
                    password='harrypotter')

# We need to add to the session or it won't ever be stored
db.session.add(passenger)

passenger = Passenger(firstname='Ron',
                    lastname='Weasley',
                    email='ron@gmail.com',
                    password='ronweasley')

# We need to add to the session or it won't ever be stored
db.session.add(passenger)


passenger = Passenger(firstname='Draco',
                    lastname='Malfoy',
                    email='draco@gmail.com',
                    password='dracoemalfoy')

# We need to add to the session or it won't ever be stored
db.session.add(passenger)

passenger = Passenger(firstname='Hermoine',
                    lastname='Granger',
                    email='hermoine@gmail.com',
                    password='hermoinegranger')

# We need to add to the session or it won't ever be stored
db.session.add(passenger)

# Once we're done, we should commit our work
db.session.commit()

#################################################################################
#Drivers

driver = Driver(firstname=NULL,
                    lastname='Snape',
                    driver_location='Forbidden Forest',
                    email='snape@gmail.com',
                    password='professorsnape')

# We need to add to the session or it won't ever be stored
db.session.add(driver)

driver = Driver(firstname='Professor',
                    lastname='Dumbledore',
                    driver_location='Kings Cross Station, Platform 9.75',
                    email='dumbledore@gmail.com',
                    password='professordumbledore')

# We need to add to the session or it won't ever be stored
db.session.add(driver)

driver = Driver(firstname=NULL,
                    lastname='Hagrid',
                    driver_location='Gringotts',
                    email='hagrid@gmail.com',
                    password='hagrid')

# We need to add to the session or it won't ever be stored
db.session.add(driver)

driver = Driver(firstname='Neville',
                    lastname='Longbottom',
                    driver_location='Grimmauld Place',
                    email='neville@gmail.com',
                    password='nevillelongbottom')

# We need to add to the session or it won't ever be stored
db.session.add(driver)

#################################################################################
#Rides

ride = Ride(passenger_location='Forbidden Forest',
                    passenger_destination='Ministry of Magic',
                    pick_up_time='2016-06-12 13:00:00')

# We need to add to the session or it won't ever be stored
db.session.add(ride)

ride = Ride(passenger_location='Hogwarts',
                    passenger_destination='Malfoy Mansion',
                    pick_up_time='2016-06-20 16:00:00')


# We need to add to the session or it won't ever be stored
db.session.add(ride)

ride = Ride(passenger_location='Malfoy Mansion',
                    passenger_destination='Hogwarts',
                    pick_up_time='2016-06-20 16:15:00')


# We need to add to the session or it won't ever be stored
db.session.add(ride)

ride = Ride(passenger_location='Grimmauld Place',
                    passenger_destination='Diagon Alley',
                    pick_up_time='2016-07-4 11:30:00')

# We need to add to the session or it won't ever be stored
db.session.add(ride)



# Once we're done, we should commit our work
db.session.commit()










#import datetime







if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    
