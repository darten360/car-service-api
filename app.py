import datetime
import os

import uuid
from functools import wraps

import jwt
from _socket import gethostname
from flasgger import Swagger
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from models import basedir, db, User, Car, Gearbox
from models import (
    TypeOfTransport,
    Area,
    BodyType,
    Brand,
    City,
    Color,
    Country,
    DriveType,
    FuelType,
    Model,
    Option,
    Seller,
)
from schemas import (
    CarSchema,
    UserView,
    RegisterView,
    LoginView,
    CarsView,
    CarView,
    CreateSellerView,
    ListSellerView,
    DeleteSellerView,
)

app = Flask(__name__)

swag = Swagger(app)

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "db.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SWAGGER"] = {"title": "Cars API", "uiversion": 3, "openapi": "3.0.2"}

SQLAlchemy().init_app(app)

car_schema = CarSchema(many=False)
cars_schema = CarSchema(many=True)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]

        if not token:
            return make_response("a valid token is missing", 401)

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "token is invalid"})

        return f(current_user, *args, **kwargs)

    return decorator


@app.route("/cars", methods=["GET"])
@token_required
def get_cars(current_user):
    all_cars = Car.query.all()
    result = cars_schema.dump(all_cars)
    if result:
        return jsonify(result)
    return jsonify({"message": "list is empty"})


@app.route("/car", methods=["POST"])
@token_required
def add_cars(current_user):
    type_of_transport = (
        TypeOfTransport.query.filter_by(name=request.form["type_of_transport"])
        .first()
        .id
    )
    body_type = BodyType.query.filter_by(name=request.form["body_type"]).first().id
    brand = Brand.query.filter_by(name=request.form["brand"]).first().id
    model = Model.query.filter_by(name=request.form["model"]).first().id
    area = Area.query.filter_by(name=request.form["area"]).first().id
    city = City.query.filter_by(name=request.form["city"]).first().id
    drive_type = DriveType.query.filter_by(name=request.form["drive_type"]).first().id
    fuel_type = FuelType.query.filter_by(name=request.form["fuel_type"]).first().id
    gearbox = Gearbox.query.filter_by(name=request.form["gearbox"]).first().id
    option = Option.query.filter_by(name=request.form["option"]).first().id
    color = Color.query.filter_by(name=request.form["color"]).first().id
    country = Country.query.filter_by(name=request.form["country"]).first().id

    new_car = Car(
        type_of_transport_id=type_of_transport,
        body_type_id=body_type,
        brand_id=brand,
        model_id=model,
        area_id=area,
        city_id=city,
        drive_type_id=drive_type,
        fuel_type_id=fuel_type,
        gearbox_id=gearbox,
        option_id=option,
        color_id=color,
        country_id=country,
        seller_id=current_user.id,
    )

    db.session.add(new_car)
    db.session.commit()

    return jsonify(car_schema.dump(new_car))


@app.route("/register", methods=["POST"])
def signup_user():
    username = request.form["username"]
    password = request.form["password"]

    data = {}
    data["username"] = username
    data["password"] = password

    hashed_password = generate_password_hash(password=data["password"], method="sha256")
    new_user = User(
        public_id=str(uuid.uuid4()),
        username=data["username"],
        password=hashed_password,
        admin=False,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "registered successfully"})


@app.route("/login", methods=["POST"])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        try:
            username = request.form["username"]
            password = request.form["password"]

            user = User.query.filter_by(username=username).first()

            if check_password_hash(user.password, password):
                token = jwt.encode(
                    {
                        "public_id": user.public_id,
                        "exp": datetime.datetime.utcnow()
                        + datetime.timedelta(minutes=5),
                    },
                    app.config["SECRET_KEY"],
                )

                return jsonify({"token": token})

        except KeyError:
            return make_response(
                "sdf not verify",
                401,
                {"WWW.Authentication": 'Basic realm: "login required"'},
            )

    if auth.username and auth.password:
        user = User.query.filter_by(username=auth.username).first()

        if check_password_hash(user.password, auth.password):
            token = jwt.encode(
                {
                    "public_id": user.public_id,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                },
                app.config["SECRET_KEY"],
            )
            return jsonify({"token": token})

    return make_response(
        "could not verify", 401, {"WWW.Authentication": 'Basic realm: "login required"'}
    )


@app.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()

    result = []

    for user in users:
        user_data = {}
        user_data["public_id"] = user.public_id
        user_data["username"] = user.username
        user_data["password"] = user.password
        user_data["admin"] = user.admin

        result.append(user_data)

    return jsonify({"users": result})


@app.route("/seller", methods=["POST"])
@token_required
def create_seller(current_user):
    full_name = request.form["full_name"]

    new_sellers = Seller(full_name=full_name, user_id=current_user.id)
    db.session.add(new_sellers)
    db.session.commit()
    return jsonify({"message": "new seller created"})


@app.route("/sellers", methods=["GET"])
@token_required
def get_sellers(current_user):
    sellers = Seller.query.filter_by(user_id=current_user.id).all()

    output = []
    for seller in sellers:
        seller_data = {}
        seller_data["full_name"] = seller.full_name
        seller_data["id"] = seller.id

        output.append(seller_data)

    return jsonify({"list_of_sellers": output})


@app.route("/seller", methods=["DELETE"])
@token_required
def delete_author(current_user):
    full_name = request.form["full_name"]
    if ":" in full_name:
        seller = Seller.query.filter_by(
            full_name=full_name[: full_name.index(":")]
        ).first()
    else:
        seller = Seller.query.filter_by(full_name=full_name).first()

        if seller.user_id != current_user.id:
            raise Exception("You cannot delete this seller!")

        if not seller:
            return jsonify({"message": "seller does not exist"})

        db.session.delete(seller)

    db.session.commit()

    return jsonify({"message": "Seller deleted"})


app.add_url_rule("/cars", view_func=CarsView.as_view("cars"), methods=["GET"])

app.add_url_rule("/car", view_func=CarView.as_view("car"), methods=["POST"])

app.add_url_rule(
    "/register", view_func=RegisterView.as_view("register"), methods=["POST"]
)

app.add_url_rule("/users", view_func=UserView.as_view("users"), methods=["GET"])

app.add_url_rule("/login", view_func=LoginView.as_view("login"), methods=["POST"])

app.add_url_rule(
    "/seller", view_func=CreateSellerView.as_view("seller"), methods=["POST"]
)

app.add_url_rule(
    "/sellers", view_func=ListSellerView.as_view("sellers"), methods=["GET"]
)

app.add_url_rule(
    "/seller", view_func=DeleteSellerView.as_view("delete_seller"), methods=["DELETE"]
)

if __name__ == "__main__":
    db.create_all()
    if "liveconsole" not in gethostname():
        app.run()
