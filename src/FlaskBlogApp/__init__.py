from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
app = Flask(__name__)

app.config["SECRET_KEY"] = "6870e40e95eada2076052023834a2ce5"
app.config['WTF_CSRF_SECRET_KEY'] = 'fe9d487ba2c9a1f13a5d72fa0d76d3fb'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_course_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
from FlaskBlogApp import routes, models