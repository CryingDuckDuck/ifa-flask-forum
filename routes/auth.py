from flask import render_template, redirect, flash, request
from flask_login import login_required, logout_user, login_user
from flask_wtf import FlaskForm
from sqlalchemy.orm import joinedload
from wtforms import PasswordField, BooleanField, StringField, SubmitField
from wtforms.validators import Email, Length, InputRequired

from app import app, login_manager
from models import User


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[InputRequired("Bitte geben Sie eine Mailadresse an"), Length(1, 64), Email()])
    password = PasswordField("Passwort", validators=[InputRequired()])
    remember_me = BooleanField("Eingeloggt bleiben")
    submit = SubmitField("Anmelden")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)


@login_manager.user_loader
def load_user(user_id):
    return User.query.options(joinedload("role")).get(user_id)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        else:
            flash("Ungültige Logindaten")
    return render_template('login.html', form=form)
