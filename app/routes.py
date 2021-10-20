import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# dummy posts
posts = [
    # List's
    {
        'author': 'Emilian Constantin',
        'title': 'Blog Post 1',
        'content': 'First post content!',
        'date_posted': 'June 10, 2021'
    },
    {
        'author': 'Diana Andreia',
        'title': 'Blog Post 2',
        'content': 'Second post content!',
        'date_posted': 'June 12, 2021'
    }
]


@app.route('/')
def home():
    return render_template('index.html', title="Home")


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/blog')
def blog():  # ☟ Put the post in HTML page
    return render_template('blog.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # The user is sanded to home page after log in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Make a form instance
    form = RegistrationForm()

    # Create a validation for submit form with user name and if validate ok,
    # send the user to home page with a success message
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! {form.username.data},'
              f' you are now able to log in!', 'success')
        return redirect(url_for('login'))

    # Pass title and the form instance                              ⤵︎
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # The user is sanded to home page after log in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Make a form instance from forms.py
    form = LoginForm()

    # Create a validation for submit form with user name and if validate ok,
    # send the user to home page with a success message
    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first()
        username = User.query.filter_by(username=form.username.data).first()
        if username and email and bcrypt.check_password_hash(email.password, form.password.data):
            login_user(email, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username, email and password', 'danger')

    # Pass title and the form instance                              ⤵︎
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Update pictures and save it in database
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.split(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    # Resize picture
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
