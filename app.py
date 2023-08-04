from flask import Flask, render_template, request, redirect, session, flash
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, RadioField, SubmitField, PasswordField, SelectField, DecimalField, TextAreaField, BooleanField, FieldList, FormField, EmailField, FileField, validators
from flask_sqlalchemy import SQLAlchemy
from flask_hashing import Hashing
from sqlalchemy_utils import database_exists
from werkzeug.utils import secure_filename
from flask_wtf.file import FileRequired, FileAllowed
import random
import string
import os
import json

app = Flask(__name__)
app.secret_key = "gcf1pak5PHQ6twh@yha"
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
hash = Hashing(app)

# --- DATABASE ---
# Film
class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    film_type = db.Column(db.String, nullable=False)
    formats = db.Column(db.String, nullable=False)
    origin = db.Column(db.String, nullable=False)
    process = db.Column(db.String, nullable=False)
    film_speed = db.Column(db.Integer, nullable=False)
    grain = db.Column(db.String, nullable=False)
    contrast = db.Column(db.String, nullable=False)
    facts = db.Column(db.Text, nullable=True)
    image = db.Column(db.String, nullable=True)

    def __init__(self, brand, name, film_type, formats, origin, process, film_speed, grain, contrast, facts, image):
        self.brand = brand
        self.name = name
        self.film_type = film_type
        self.formats = formats
        self.origin = origin
        self.process = process
        self.film_speed = film_speed
        self.grain = grain
        self.contrast = contrast
        self.facts = facts
        self.image = image

# User
class User(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    pass_hash = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, username, email, pass_hash, admin):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.pass_hash = pass_hash
        self.admin = admin
# --- END DATABASE ---

# --- FORMS ---
class LoginForm(FlaskForm):
    username = StringField("User name", [validators.DataRequired(), validators.Regexp('^[a-zA-Z]+$', message="Username must contain only letters"), validators.length(min=1)])
    password = PasswordField("Password", [validators.DataRequired(), validators.length(min=6, message='Too short')])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField("First name", [validators.DataRequired(), validators.Regexp('^[a-zA-Z]+$', message="First name must contain only letters"), validators.length(min=1)], render_kw={"placeholder": "First Name"})
    last_name = StringField("Last name", [validators.DataRequired(), validators.Regexp('[a-zA-Z]', message="Last name must contain only letters"), validators.length(min=1)], render_kw={"placeholder": "Last Name"})
    username = StringField("User name", [validators.DataRequired(), validators.Regexp('^[a-zA-Z]+$', message="Username must contain only letters"), validators.length(min=1)], render_kw={"placeholder": "Username"})
    email = EmailField("Email", [validators.DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField("Password", [validators.DataRequired(), validators.length(min=6, message='Too short')], render_kw={"placeholder": "Password"})
    confirm = PasswordField("Confirm Password", [validators.EqualTo('password', 'Passwords are not the same')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Register')
# --- END FORMS ---


# --- APP ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if not user:
            flash("Username doesn't exist. Please register :)")
            return redirect('/register')
        if hash.check_value(user.pass_hash, login_form.password.data, salt=login_form.username.data):
            session['user_id'] = user.id
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            session['username'] = user.username
            session['admin'] = user.admin
            return redirect('/')
        else:
            flash('Incorrect username and/or password')

    return render_template('login.html', form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if session['user_id']:
            return redirect('/')
    except KeyError:
        pass
    
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        if User.query.filter_by(username=register_form.username.data).first():
            flash('Username already exists!')
        else:
            first_name = register_form.first_name.data
            last_name = register_form.last_name.data
            username = register_form.username.data
            email = register_form.email.data
            pass_hash = hash.hash_value(register_form.password.data, salt=username)
            admin = False
            new_user = User(first_name, last_name, username, email, pass_hash, admin)
            db.session.add(new_user)
            db.session.commit()
            db.session.refresh(new_user)
            session['user_id'] = new_user.id
            session['admin'] = new_user.admin
            return redirect('/')

    return render_template('register.html', form=register_form)


@app.route('/logout')
def logout():
    session.clear()

    return redirect('/')


@app.route('/film-index')
def film_index():
    query = Film.query

    for key, value in request.args.items():
        query = query.filter(getattr(Film, key).like(f'%{value}%'))
    films = query.all()

    return render_template('film-index.html', films=films)


@app.route('/film/<id>')
def film(id):
    film = Film.query.get(id)

    return render_template('film.html', film=film)


@app.route('/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()

    return render_template('user.html', user=user)


with app.app_context():
    db.create_all()