from flask import render_template
from sqlalchemy.orm import joinedload

from app import app
from models import Post


@app.route("/")
def all_posts():
    posts = Post.query.options(joinedload("user")).all()
    return render_template("posts/index.html", posts=posts)


@app.route("/posts/<post_id>")
def post_by_id(post_id):
    post = Post.query.options(joinedload("user"), joinedload("comments"), joinedload("comments.user")).get(post_id)
    return render_template("posts/id.html", post=post)