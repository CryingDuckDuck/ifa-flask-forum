from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_prefixed_env()
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

from routes import *
from models import *
from filters import *
from commands import *
