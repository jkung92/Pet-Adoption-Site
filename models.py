"""Models for Adopt."""
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, TextAreaField
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import InputRequired, Optional, URL, AnyOf, Length, NumberRange

db = SQLAlchemy()


def connect_db(app):
    """ Connect to database. """
    db.app = app
    db.init_app(app)


class Pet(db.Model):
    """ Model for a pet available for adoption """
    __tablename__ = "pets"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.UnicodeText, nullable=False)
    species = db.Column(db.UnicodeText, nullable=False)
    photo_url = db.Column(
        db.UnicodeText, nullable=True, default="/static/Not-available.gif")
    age = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.UnicodeText, nullable=True)
    available = db.Column(db.Boolean, nullable=False, default=True)


class AddPetForm(FlaskForm):
    """ Form for adding pets. """
    name = StringField("Pet Name", validators=[InputRequired()])
    species = StringField(
        "Species Name", validators=[AnyOf(['cat', 'dog', 'porcupine'])])
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    age = FloatField(
        "Pet Age",
        validators=[
            NumberRange(min=0, max=30, message='Age must be between 0 and 30')
        ])
    notes = TextAreaField("Notes", validators=[Length(min=0, max=255)])


class EditPetForm(FlaskForm):
    """ Form for editing pets. """
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    notes = StringField("Notes")
    available = BooleanField("Availability")