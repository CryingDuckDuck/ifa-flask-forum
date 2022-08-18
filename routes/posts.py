from flask import jsonify, render_template
from sqlalchemy.orm import joinedload

from app import app
from models import Post, User


@app.route("/")
def all_posts():
    posts = Post.query.options(joinedload("user")).all()
    users = User.query.all()
    return render_template("index.html", posts=posts, users=users)
