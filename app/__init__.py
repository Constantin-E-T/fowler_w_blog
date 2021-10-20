from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_moment import Moment

app = Flask(__name__)
# Create a secret key ❖ to create one very easy go to python console log and
# >>> import secrets
# >>> secrets.token_hex(ex:16)
app.config['SECRET_KEY'] = '1acff3c0d6ebf1dd037206a55d48024a'
# Create database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# SQLAlchemy error muted
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Create db variable
db = SQLAlchemy(app)
# Brypt instance
bcrypt = Bcrypt(app)
# Login manager instance
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# Date time instance
moment = Moment(app)

from app import routes
