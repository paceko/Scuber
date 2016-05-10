from model import Ride, Passenger, Driver, connect_to_db, db
from server import app

"""Utility file to seed passengers (users)"""




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

#################################################################################
#Drivers

driver = Driver(firstname='Professor',
                    lastname='Snape',
                    email='snape@gmail.com',
                    password='professorsnape')




# Once we're done, we should commit our work
db.session.commit()










#import datetime







if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    
