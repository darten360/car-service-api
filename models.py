import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SECRET_KEY"] = "adfadf7878s8df7asdf"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "db.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Car(db.Model):
    __tablename__ = "cars"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    datetime_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    type_of_transport_id = db.Column(db.Integer, db.ForeignKey("types_of_transport.id"))
    body_type_id = db.Column(db.Integer, db.ForeignKey("body_types.id"))
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id"))
    model_id = db.Column(db.Integer, db.ForeignKey("models.id"))
    area_id = db.Column(db.Integer, db.ForeignKey("areas.id"))
    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"))
    drive_type_id = db.Column(db.Integer, db.ForeignKey("drive_types.id"))
    fuel_type_id = db.Column(db.Integer, db.ForeignKey("fuel_types.id"))
    gearbox_id = db.Column(db.Integer, db.ForeignKey("gearboxes.id"))
    seller_id = db.Column(db.Integer, db.ForeignKey("sellers.id"))
    option_id = db.Column(db.Integer, db.ForeignKey("options.id"))
    color_id = db.Column(db.Integer, db.ForeignKey("colors.id"))
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"))


class TypeOfTransport(db.Model):
    __tablename__ = "types_of_transport"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.relationship(
        "Car", backref="types_of_transport", lazy=True, cascade="all, delete"
    )
    name = db.Column(db.String(50), nullable=False)


class BodyType(db.Model):
    __tablename__ = "body_types"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.relationship(
        "Car", backref="body_types", lazy=True, cascade="all, delete"
    )
    name = db.Column(db.String(50), nullable=False)


class Brand(db.Model):
    __tablename__ = "brands"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand = db.relationship("Car", backref="brands", lazy=True, cascade="all, delete")
    name = db.Column(db.String(50), nullable=False)


class Model(db.Model):
    __tablename__ = "models"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model = db.relationship("Car", backref="models", lazy=True, cascade="all, delete")
    name = db.Column(db.String(50), nullable=False)


class Area(db.Model):
    __tablename__ = "areas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    area = db.relationship("Car", backref="areas", lazy=True, cascade="all, delete")
    name = db.Column(db.String(50), nullable=False)


class City(db.Model):
    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city = db.relationship("Car", backref="cities", lazy=True, cascade="all, delete")
    name = db.Column(db.String(50), nullable=False)


class DriveType(db.Model):
    __tablename__ = "drive_types"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    drive_type = db.relationship(
        "Car", backref="drive_types", lazy=True, cascade="all, delete"
    )
    name = db.Column(db.String(50), nullable=False)


class FuelType(db.Model):
    __tablename__ = "fuel_types"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fuel = db.relationship(
        "Car", backref="fuel_types", lazy=True, cascade="all, delete"
    )
    name = db.Column(db.String(50), nullable=False)


class Gearbox(db.Model):
    __tablename__ = "gearboxes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    box = db.relationship("Car", backref="gearboxes", lazy=True, cascade="all, delete")
    name = db.Column(db.String(50), nullable=False)


class Option(db.Model):
    __tablename__ = "options"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    option = db.relationship("Car", backref="options", lazy=True, cascade="all, delete")
    name = db.Column(db.String(50), nullable=False)


class Color(db.Model):
    __tablename__ = "colors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    color = db.relationship("Car", backref="colors", lazy=True, cascade="all, delete")
    name = db.Column(db.String(50), nullable=False)


class Country(db.Model):
    __tablename__ = "countries"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country = db.relationship(
        "Car", backref="countries", lazy=True, cascade="all, delete"
    )
    name = db.Column(db.String(50), nullable=False)


class Seller(db.Model):
    __tablename__ = "sellers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cars = db.relationship("Car", backref="sellers", lazy=True, cascade="all, delete")
    full_name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)


class User(db.Model):
    __tablename__ = "users"
    public_id = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String())
    admin = db.Column(db.Boolean)
