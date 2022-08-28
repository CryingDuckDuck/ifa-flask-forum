from sqlalchemy import func

from app import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="comments")
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    post = db.relationship("Post")

    def __repr__(self):
        return '<Comment %r>' % self.text
