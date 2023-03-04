from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from dotenv import load_dotenv
import os
from flaskbook_app.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


db = SQLAlchemy()

DB_NAME = "database.db"



app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

from .main.routes import main
from .auth.routes import auth

app.register_blueprint(main, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

from .models import User, Post, Comment, Follow

with app.app_context():
    db.create_all()


bcrypt = Bcrypt(app)


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
