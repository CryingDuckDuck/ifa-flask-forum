from flask import render_template, redirect, flash, request
from flask_login import login_required, logout_user, login_user
from flask_wtf import FlaskForm
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from wtforms import PasswordField, BooleanField, StringField, SubmitField
from wtforms.validators import Email, Length, InputRequired, EqualTo

from app import app, login_manager, db
from models import User, Role


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[InputRequired("Bitte geben Sie eine Mailadresse an"), Length(1, 64), Email()])
    password = PasswordField("Passwort", validators=[InputRequired("Bitte geben Sie ein Passwort an")])
    remember_me = BooleanField("Eingeloggt bleiben")
    submit = SubmitField("Anmelden")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)


class RegistrationForm(FlaskForm):
    username = StringField('Benutzername',
                           validators=[InputRequired("Bitte geben Sie einen Benutzernamen an"), Length(1, 64)])
    email = StringField('Email',
                        validators=[InputRequired("Bitte geben Sie eine Mailadresse an"), Length(1, 64), Email()])
    password = PasswordField("Passwort",
                             validators=[InputRequired("Bitte geben Sie ein Passwort ein"), EqualTo('confirm_password', message='Passwörter stimmen nicht überein')])
    confirm_password = PasswordField("Passwort bestätigen", validators=[InputRequired("Passwörter stimmen nicht überein")])
    submit = SubmitField("Registrieren")

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)


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
    return render_template('auth/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter(or_(User.email == form.email.data, User.username == form.username.data)).first()
        if user:
            flash("Ungültige Daten")
        else:
            email = form.email.data
            username = form.username.data
            password = form.password.data
            role = Role.query.filter_by(name="user").first()
            new_user = User(email=email, username=username, password=password, role=role)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
    return render_template('auth/register.html', form=form)
