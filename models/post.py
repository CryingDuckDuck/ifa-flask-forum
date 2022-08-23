from datetime import datetime
import pytz

from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, unique=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime(), nullable=False, default=lambda: datetime.now(pytz.timezone("Europe/Zurich")))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="posts")

    def __repr__(self):
        return '<Post %r>' % self.title
