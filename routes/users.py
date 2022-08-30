from flask import render_template, abort, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from sqlalchemy.orm import joinedload
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.widgets import HiddenInput

from app import app, db
from models import Post, User, Role


class UserRoleForm(FlaskForm):
    user_id = IntegerField(widget=HiddenInput())
    role = SelectField("Role", coerce=int)
    submit = SubmitField("Role ändern")

    def __init__(self, *args, **kwargs):
        super(UserRoleForm, self).__init__(*args, **kwargs)


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

    form = UserRoleForm()
    roles = Role.query.all()
    form.role.choices = [(r.id, r.name) for r in roles]

    if form.validate_on_submit():
        user = User.query.get(form.user_id.data)

        if user is None:
            return abort(404)

        user.role_id = form.role.data
        db.session.commit()
        form.role.data = 0
        flash(f"Role des Benutzers {user.username} wurde geändert!")

    users = User.query.options(joinedload("role")).all()
    return render_template("users/manage.html", users=users, form=form)
