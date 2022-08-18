from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_prefixed_env()
db = SQLAlchemy(app)

from routes import *
from models import *

db.create_all()

db.session.bulk_save_objects([
    Role(name="admin"),
    Role(name="user")
])
db.session.commit()

# bulk_save_objects won't trigger events (user => before_insert)
db.session.add(
    User(email="admin@admin.ch", password="password", username="admin", role_id=1)
)
db.session.add(
    User(email="user@user.ch", password="password", username="user", role_id=2)
)
db.session.commit()

db.session.bulk_save_objects([
    Post(title="test post", body="post bodybodybodybodybodybodybodybodybodybodybodybodybodybodybodybodybodybodybodybody", user_id=1),
    Post(title="test post 2", body="post bodybodybodybodybodybodybodybodybodybodybodybodybodybodybodybodybodybodybodybody", user_id=1),
    Post(title="test post 3", body="post bodybodybodybodybodybodybodybodybodybodybodybodybodybodybodybodybodybodybodybody", user_id=1)
])
db.session.commit()