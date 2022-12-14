from bcrypt import hashpw, gensalt, checkpw
from flask_login import UserMixin
from sqlalchemy import event

from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.TEXT, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("Role")
    posts = db.relationship("Post", back_populates="user")
    comments = db.relationship("Comment", back_populates="user")

    @property
    def is_admin(self):
        return self.role.name.lower() == "admin"

    def check_password(self, password):
        return checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def __repr__(self):
        return '<User %r>' % self.username


def hash_password(mapper, connection, target):
    target.password = hashpw(target.password.encode("utf-8"), gensalt(10)).decode("utf-8")


event.listen(User, "before_insert", hash_password)
