from flask import render_template
from flask_login import login_required
from sqlalchemy.orm import joinedload

from app import app
from models import Post, User


@app.route("/")
@login_required
def all_posts():
    posts = Post.query.options(joinedload("user")).all()
    users = User.query.all()
    return render_template("index.html", posts=posts, users=users)


@app.route("/posts/<slug>")
def post_by_slug(slug):
    return "post by slug"


@app.route("/posts/create")
def create_post():
    return "create post"


@app.route("/posts/<slug>/edit")
def edit_post():
    return "edit post"