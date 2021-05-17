from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os

#initializing our flask app
app = Flask(__name__)

# setting up our base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# setting up our database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# initialize our db
db = SQLAlchemy(app)

# initialize marshmallow
ma = Marshmallow(app)

# creating our model is class product

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)


    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

# product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'descrption', 'price', 'qty')


# let's initialize our schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# creating our routes
# create a product

@app.route("/product", methods=['POST'])
def app_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)

    db.session.add(new_product)

    # commiting/saving it to the database
    db.session.commit()

    return product_schema.jsonify(new_product)


# Get all products
@app.route("/products", methods=['GET'])
def fetch_products():
    all_products = Product.query.all()
    results = products_schema.dump(all_products)
    return jsonify(results)


@app.route("/product/<id>", methods=['GET'])
def fetch_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)    

@app.route("/product/<id>", methods=['GET'])
def fetch_products(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


# run our server
if __name__ == "__main__":
    app.run(debug=True)