
from models import User, Post, PostTag, Tag, db
from app import app

# Create All Tables
db.drop_all()
db.create_all()


User.query.delete()
Post.query.delete()
PostTag.query.delete()
Tag.query.delete()

#Add Sample Users
bruce = User(first_name="Bruce", last_name="Wayne")
peter = User(first_name="Peter", last_name="Parker")
eddie = User(first_name="Eddie", last_name="Brock")
barry = User(first_name="Barry", last_name="Allen")

#Add Sample Posts
bpost = Post(title="Dark Knight", content="I am Batman!", user_id="1")
ppost = Post(title="Web Slinger", content="Your friendly neighborhood Spider-Man", user_id="2")
epost = Post(title="I am Eddie", content="We Are Venom.", user_id="3")
bapost = Post(title="Catch Me", content="'My name is Barry Allen and I am the fastest man alive", user_id="4")

db.session.add_all([bruce, peter, eddie, barry, bpost, ppost, epost, bapost])
db.session.commit()

#Add Sample Tags
tbruce = Tag(name="Billionare")
tbruceTwo = Tag(name="Crime Fighter")
tpeter = Tag(name="New York")
tpeterTwo = Tag(name="Spidey Senses")
teddie = Tag(name="Villian")
teddieTwo = Tag(name="Evil")
tbarry = Tag(name="Fast")
tbarryTwo = Tag(name="Speed")


db.session.add_all([tbruce, tbruceTwo, tpeter, tpeterTwo, teddie, teddieTwo, tbarry, tbarryTwo])
db.session.commit()
