from sqlalchemy import func

from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, unique=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="posts")

    def __repr__(self):
        return '<Post %r>' % self.title
