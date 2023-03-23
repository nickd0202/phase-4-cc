from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)
# Add models here

class Pizza(db.Model, SerializerMixin):

    __tablename__ = 'pizzas'

    serialize_rules = ('-pizza_restaurants.pizza', '-restaurants.pizzas')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    pizza_restaurants = db.relationship('RestaurantPizza', backref = 'pizza')
    restaurants = association_proxy('pizza_restaurants', 'restaurant')

class Restaurant(db.Model, SerializerMixin):

    __tablename__ = 'restaurants'

    serialize_rules = ('-pizza_restaurants.restaurant', '-pizzas.restaurants')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    pizza_restaurants = db.relationship('RestaurantPizza', backref = 'restaurant')
    pizzas = association_proxy('pizza_restaurants', 'pizza')

class RestaurantPizza(db.Model, SerializerMixin):

    __tablename__ = 'restaurant_pizzas'

    serialize_rules = ('-pizza.pizza_restaurants', '-restaurant.pizza_restaurants')

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    @validates('price')
    def validates_price(self, key, value):
        if value <= 1 or value >= 30:
            raise ValueError('Price must be between 1 and 30')
        return value
    