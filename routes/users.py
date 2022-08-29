from flask import render_template, abort
from flask_login import login_required, current_user

from app import app
from models import Post


@app.route("/profile")
@login_required
def profile():
    posts = Post.query.where(Post.user_id == current_user.id).order_by(Post.posted_at.desc()).all()
    return render_template("users/profile.html", posts=posts)


@app.route("/users/manage", methods=["GET", "POST"])
@login_required
def manage_users():
    if not current_user.is_admin:
        return abort(401)

    return render_template("users/manage.html")