from unittest import TestCase

from app import app
from models import db, User, Post, Tag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_fake_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserTest(TestCase):

    def setUp(self):
        """ Add Fake User """

        User.query.delete()

        user = User(first_name="Test", last_name="One", image_url="http://google.com")
        bpost = Post(title="Dark Knight", content="I am Batman!", user_id="1")
        tbruce = Tag(name="Billionare")
        db.session.add(bpost)
        db.session.add(tbruce)
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test One</h1>', html)

    def test_show_tag(self):
        with app.test_client() as client:
            resp = client.get(f"/tags/{self.tag_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1>Billionare</h1>', html)