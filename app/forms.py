from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


# Create a class module
class RegistrationForm(FlaskForm):
    # Make the username field
    username = StringField('Username',
                           # ▶︎   Create also validators, and the length of username
                           validators=[DataRequired(), Length(min=2, max=20)])
    # Make the email field
    email = StringField('Email',
                        # ▶︎   Insert data and what kind of data
                        validators=[DataRequired(), Email()])
    # Make the password field
    password = PasswordField('Password',
                             # ▶︎   Create also validators, and the length of password
                             validators=[DataRequired(), Length(min=4, max=12)])
    # Make the confirm password field
    confirm_password = PasswordField('Confirm Password',
                                     # ▶︎   Create also validators, has to be equal to password ↰
                                     validators=[DataRequired(), EqualTo('password')])
    # Submit btn
    submit = SubmitField('Sign Up')

    # Give a feedback to the user if on register will feel the form with an already username and email are taken.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one! ')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one! ')


# Create a class module
class LoginForm(FlaskForm):
    # Make the username field
    username = StringField('Username',
                           # ▶︎   Create also validators, and the length of username
                           validators=[DataRequired(), Length(min=2, max=20)])
    # # Make the email field
    email = StringField('Email',
                        # ▶︎   Insert data and what kind of data
                        validators=[DataRequired(), Email()])
    # Make the password field
    password = PasswordField('Password',
                             # ▶︎   Create also validators, and the length of password
                             validators=[DataRequired(), Length(min=4, max=12)])
    # Make a remember field
    remember = BooleanField('Remember Me')
    # Login btn
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    # Make the username field
    username = StringField('Username',
                           # ▶︎   Create also validators, and the length of username
                           validators=[DataRequired(), Length(min=2, max=20)])
    # Make the email field
    email = StringField('Email',
                        # ▶︎   Insert data and what kind of data
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    # Submit btn
    submit = SubmitField('Update')

    # Give a feedback to the user if on register will feel the form with an already username and email are taken.
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one! ')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one! ')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
