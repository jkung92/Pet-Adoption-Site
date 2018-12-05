"""Adopt application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db
from flask_debugtoolbar import DebugToolbarExtension
from models import Pet, AddPetForm, EditPetForm
from flask_sqlalchemy import SQLAlchemy
from secrets import API_Secret, API_Key, db_url
from petfinder import get_random_pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)


@app.route("/")
def list_pets():
    """ Should list pet name, photo(if present), display availibility"""
    available_pets = Pet.query.filter(Pet.available).all()
    unavailable_pets = Pet.query.filter(Pet.available == False).all()
    random_pet = get_random_pet()
    return render_template(
        "index.html",
        pets=available_pets,
        unavailable_pets=unavailable_pets,
        random_pet=random_pet)


@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """ Pet add form; handle adding."""
    form = AddPetForm()

    if form.validate_on_submit():
        form_data = form.data.copy()
        form_data.pop("csrf_token", None)

        pet = Pet(**form_data)

        db.session.add(pet)
        db.session.commit()
        flash(f"{pet.name} was added!")
        return redirect("/")

    else:
        return render_template("add_pet.html", form=form, button_label="Add")


@app.route("/<int:pid>", methods=["GET", "POST"])
def edit_pet(pid):
    """ Show pet edit form and handle edit. """
    pet = Pet.query.get_or_404(pid)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        flash(f"Pet {pet.name} updated!")
        return redirect(f"/{pid}")
    else:
        return render_template(
            "edit_pet.html", form=form, pet=pet, button_label="Submit")
