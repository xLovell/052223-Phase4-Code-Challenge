#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants', methods=['GET'])
def restaurants():
    restaurants = []
    for restaurant in Restaurant.query.all():
        restaurants.append(restaurant.to_dict(rules=("-restaurant_pizzas",)))
    return make_response(restaurants, 200)

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def restaurants_by_id(id):
    restaurant=Restaurant.query.filter(Restaurant.id == id).first()

    if restaurant == None:
        return make_response({"error": "Restaurant not found"}, 404)
    else:
        if request.method == 'GET':
            return make_response(restaurant.to_dict(), 200)
        
        elif request.method == 'DELETE':
            db.session.delete(restaurant)
            db.session.commit()

            return make_response({}, 204)
        
@app.route('/pizzas')
def pizzas():
    pizzas=[]
    for pizza in Pizza.query.all():
        pizzas.append(pizza.to_dict(rules=("-restaurant_pizzas",)))
    return make_response(pizzas, 200)

@app.route('/restaurant_pizzas', methods=['POST'])
def restaurant_pizzas():
    try:
        restaurant_pizza = RestaurantPizza(
            price = request.get_json()['price'],
            pizza_id = request.get_json()['pizza_id'],
            restaurant_id = request.get_json()['restaurant_id']
        )
        db.session.add(restaurant_pizza)
        db.session.commit()

        return make_response(restaurant_pizza.to_dict(), 201)
    
    except ValueError:
        return make_response({"errors": ["validation errors"]}, 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
