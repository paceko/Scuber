import unittest

from server import app
from model import db, connect_to_db
# example_data,

class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app)


    def test_homepage(self):
        result = self.client.get("/register")
        self.assertIn("Register", result.data)

    def test_login(self):
        # FIXME: Add a test to show we see the login form, but NOT the party details
        result = self.client.get("/login")
        self.assertIn("Login", result.data)

    def test_rsvp(self):
        result = self.client.post("/login",
                                  data={'email': "harry@gmail.com", 'password': "harry"},
                                  follow_redirects=True)
     
        # FIXME: Once we login, we should see the party details, but not the RSVP form
        self.assertIn("on demand scooter ridesharing", result.data)


# class PartyTestsDatabase(unittest.TestCase):
#     """Flask tests that use the database."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         self.client = app.test_client()
#         app.config['TESTING'] = True

#         # Connect to test database (uncomment when testing database)
#         # connect_to_db(app, "postgresql:///testdb")

#         # Create tables and add sample data (uncomment when testing database)
#         # db.create_all()
#         # example_data()

#     def tearDown(self):
#         """Do at end of every test."""

#         # (uncomment when testing database)
#         # db.session.close()
#         # db.drop_all()

#     def test_games(self):
#         #FIXME: test that the games page displays the game from example_data()
#         print "FIXME"


if __name__ == "__main__":
    unittest.main()
