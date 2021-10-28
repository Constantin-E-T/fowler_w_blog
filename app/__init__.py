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
ENV = 'dev'

if ENV == 'prod':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/user_data'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://iruxkonkkwkplh' \
                                            ':c58d045aae2e119e021b220a8b791725fa7285a4942c13d8f24233b3c02fab86@ec2-52' \
                                            '-6-211-59.compute-1.amazonaws.com:5432/d6lvnffdvams5u'

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL.replace('postgres://', 'postgresql://')",
#                                                        'sqlite:///site.db')
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
