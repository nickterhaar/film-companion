from flask import Flask, render_template, request, redirect, session, Markup
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, RadioField, SubmitField, PasswordField, SelectField, DecimalField, TextAreaField, BooleanField, FieldList, FormField, EmailField, FileField, validators
from flask_sqlalchemy import SQLAlchemy
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


# --- DATABASE ---
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


with app.app_context():
    db.create_all()


# --- FORMS ---



# --- APP ---
@app.route('/')
def index():
    

    return render_template('index.html')


@app.route('/film-index')
def film_index():
    query = Film.query
    process = set()

    for key, value in request.args.items():
        query = query.filter(getattr(Film, key).like(f'%{value}%'))
    films = query.all()

    # films = Film.query.all()

    return render_template('film-index.html', films=films)


@app.route('/film-index/<filter_property>')
def black_white():
    films = Film.query.filter(Film.film_type.like('%Black & White%'))

    return render_template('film-index.html', films=films)

# @app.route('/film-index/color')
# def color():
#     films = Film.query.filter(Film.film_type.like('%Color%'))

#     return render_template('film-index.html', films=films)