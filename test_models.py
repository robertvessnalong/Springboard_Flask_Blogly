from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_fake_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserTest(TestCase):

    def setUp(self):

        User.query.delete()
    
    def tearDown(self):

        db.session.rollback()