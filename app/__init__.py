from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail
import os

app = Flask(__name__)
# Create a secret key ❖ to create one very easy go to python console log and
# >>> import secrets
# >>> secrets.token_hex(ex:16)
app.config['SECRET_KEY'] = os.environ.get("MY_SECRET_KEY")
# Create database config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL.replace('postgres://', 'postgresql://')",
                                                       'sqlite:///site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# Login manager instance
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# Date time instance
moment = Moment(app)

app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
app.config['MAIL_PORT'] = 587
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')

mail = Mail(app)

from app import routes
