from bcrypt import hashpw, gensalt, checkpw
from flask_login import UserMixin
from sqlalchemy import event

from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("Role")
    posts = db.relationship("Post", back_populates="user")

    def check_password(self, password):
        return checkpw(str.encode(password), self.password)

    def __repr__(self):
        return '<User %r>' % self.username


def hash_password(mapper, connection, target):
    target.password = hashpw(str.encode(target.password), gensalt(10))


event.listen(User, "before_insert", hash_password)
