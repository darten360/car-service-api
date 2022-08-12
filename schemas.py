from flasgger import Schema, fields, SwaggerView

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
    Gearbox,
    Seller,
    User,
)


class CarSchema(Schema):
    id = fields.Integer()
    datetime_created = fields.DateTime()
    datetime_updated = fields.DateTime()
    type_of_transport_id = fields.Integer()
    body_type_id = fields.Integer()
    brand_id = fields.Integer()
    model_id = fields.Integer()
    gearbox_id = fields.Integer()
    drive_type_id = fields.Integer()
    fuel_type_id = fields.Integer()
    city_id = fields.Integer()
    area_id = fields.Integer()
    option_id = fields.Integer()
    color_id = fields.Integer()
    country_id = fields.Integer()
    seller_id = fields.Integer()


class UserSchema(Schema):
    public_id = fields.Integer()
    username = fields.String()
    password = fields.String()
    admin = fields.Boolean()


class CarView(SwaggerView):
    parameters = [
        {
            "name": "area",
            "in": "formData",
            "type": "string",
            "required": True,
            "enum": [area.name for area in Area.query.all()],
        },
        {
            "name": "body_type",
            "in": "formData",
            "type": "string",
            "required": True,
            "enum": [body.name for body in BodyType.query.all()],
        },
        {
            "name": "brand",
            "in": "formData",
            "type": "string",
            "required": True,
            "enum": [brand.name for brand in Brand.query.all()],
        },
        {
            "name": "city",
            "in": "formData",
            "type": "string",
            "required": True,
            "enum": [city.name for city in City.query.all()],
        },
        {
            "name": "color",
            "in": "formData",
            "type": "string",
            "required": True,
            "enum": [color.name for color in Color.query.all()],
        },
        {
            "name": "country",
            "in": "formData",
            "type": "string",
            "required": True,
            "enum": [country.name for country in Country.query.all()],
        },
        {
            "name": "drive_type",
            "in": "formData",
            "type": "string",
            "required": True,
            "enum": [drive.name for drive in DriveType.query.all()],
        },
        {
            "name": "fuel_type",
            "in": "formData",
            "type": "string",
            "required": True,
            "enum": [fuel.name for fuel in FuelType.query.all()],
        },
        {
            "name": "gearbox",
            "in": "formData",
            "type": "string",
            "required": True,
            "enum": [box.name for box in Gearbox.query.all()],
        },
        {
            "name": "model",
            "in": "formData",
            "type": "string",
            "required": True,
            "enum": [model.name for model in Model.query.all()],
        },
        {
            "name": "option",
            "in": "formData",
            "type": "string",
            "required": True,
            "enum": [option.name for option in Option.query.all()],
        },
        {
            "name": "type_of_transport",
            "in": "formData",
            "type": "string",
            "required": True,
            "enum": [transport.name for transport in TypeOfTransport.query.all()],
        },
        {
            "name": "x-access-tokens",
            "in": "header",
            "description": "Put right here your JWT token",
            "type": "string",
            "required": True,
        },
        {
            "name": "Content-Type",
            "in": "header",
            "description": "Do not touch this line",
            "type": "string",
            "required": True,
            "default": "application/json",
        },
    ]
    responses = {
        200: {
            "description": "Create New Car",
        },
        400: {
            "description": "Incorrect request, try again",
        },
    }
    consumes = ["application/x-www-form-urlencoded"]


class CarsView(SwaggerView):
    parameters = [
        {
            "name": "x-access-tokens",
            "in": "header",
            "description": "Put right here your JWT token",
            "type": "string",
            "required": True,
        },
        {
            "name": "Content-Type",
            "in": "header",
            "description": "Do not touch this line",
            "type": "string",
            "required": True,
            "default": "application/json",
        },
    ]
    responses = {200: {"description": "A list of cars", "schema": CarSchema}}
    consumes = ["application/x-www-form-urlencoded"]


class UserView(SwaggerView):
    responses = {200: {"description": "Show all users", "schema": UserSchema}}


class RegisterView(SwaggerView):
    parameters = [
        {
            "name": "username",
            "in": "formData",
            "type": "string",
            "required": True,
        },
        {
            "name": "password",
            "in": "formData",
            "type": "string",
            "required": True,
        },
    ]
    responses = {200: {"description": "Register new user", "schema": UserSchema}}
    consumes = ["application/x-www-form-urlencoded"]


class LoginView(SwaggerView):
    parameters = [
        {
            "name": "username",
            "in": "formData",
            "type": "string",
            "required": True,
        },
        {
            "name": "password",
            "in": "formData",
            "type": "string",
            "required": True,
        },
    ]
    responses = {
        200: {"description": "Login User and get JWT token", "schema": UserSchema}
    }
    consumes = ["application/x-www-form-urlencoded"]


class CreateSellerView(SwaggerView):
    parameters = [
        {
            "name": "full_name",
            "in": "formData",
            "type": "string",
            "required": True,
        },
        {
            "name": "x-access-tokens",
            "in": "header",
            "description": "Put right here your JWT token",
            "type": "string",
            "required": True,
        },
        {
            "name": "Content-Type",
            "in": "header",
            "description": "Do not touch this line",
            "type": "string",
            "required": True,
            "default": "application/json",
        },
    ]
    responses = {
        200: {"description": "Login User and get JWT token", "schema": UserSchema}
    }
    consumes = ["application/x-www-form-urlencoded"]


class ListSellerView(SwaggerView):
    parameters = [
        {
            "name": "x-access-tokens",
            "in": "header",
            "description": "Put right here your JWT token",
            "type": "string",
            "required": True,
        },
        {
            "name": "Content-Type",
            "in": "header",
            "description": "Do not touch this line",
            "type": "string",
            "required": True,
            "default": "application/json",
        },
    ]
    responses = {200: {"description": "Show all users", "schema": UserSchema}}


def get_username_and_full_name():
    users = User.query.all()
    names = []
    result = []
    for user in users:
        names.append(user.username)
    for name in names:
        seller = Seller.query.filter_by(
            user_id=User.query.filter_by(username=name).first().id
        ).first()
        if seller is None:
            continue
        else:
            result.append(f"{seller.full_name}: {name}")
    return result


class DeleteSellerView(SwaggerView):
    parameters = [
        {
            "name": "full_name",
            "in": "formData",
            "type": "string",
            "description": "Seller who will be deleted",
            "required": True,
            "enum": [name for name in get_username_and_full_name()],
        },
        {
            "name": "x-access-tokens",
            "in": "header",
            "description": "Put right here your JWT token",
            "type": "string",
            "required": True,
        },
        {
            "name": "Content-Type",
            "in": "header",
            "description": "Do not touch this line",
            "type": "string",
            "required": True,
            "default": "application/json",
        },
    ]
    responses = {200: {"description": "Show all users", "schema": UserSchema}}
    consumes = ["application/x-www-form-urlencoded"]
