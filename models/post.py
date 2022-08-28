from sqlalchemy import func, select
from sqlalchemy.orm import column_property

from app import db
from models import Comment


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, unique=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="posts")

    comments = db.relationship("Comment", back_populates="post")
    comment_count = column_property(
        select([func.count(Comment.id)])
        .where(Comment.post_id == id)
        .scalar_subquery()
    )

    def __repr__(self):
        return '<Post %r>' % self.title
