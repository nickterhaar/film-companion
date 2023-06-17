from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, RadioField, SubmitField, PasswordField, SelectField, DecimalField, TextAreaField, BooleanField, FieldList, FormField, EmailField, FileField, validators
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_wtf.file import FileRequired, FileAllowed
import random
import string
import os

app = Flask(__name__)
app.secret_key = "gcf1pak5PHQ6twh@yha"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# CODE


with app.app_context():
    db.create_all()