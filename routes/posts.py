from flask import render_template
from sqlalchemy.orm import joinedload

from app import app
from models import Post


@app.route("/")
def all_posts():
    posts = Post.query.options(joinedload("user")).all()
    return render_template("posts/index.html", posts=posts)


@app.route("/posts/<slug>")
def post_by_slug(slug):
    return "post by slug"


@app.route("/posts/create")
def create_post():
    return "create post"


@app.route("/posts/<slug>/edit")
def edit_post():
    return "edit post"
