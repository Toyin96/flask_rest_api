from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os

# init app  
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.route("/", methods=["GET"])
def hello():
    return jsonify({"name": "Toyin"})

# setting up our database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)

#product class

class product(db.Model):
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
        fields = ('id', 'name', 'description', 'qty')

# init our schema
product_schema = ProductSchema() # console would give us awarning if we don't do this strict stuff
products_schema = ProductSchema(many=True) # many=True means we're dealing with more than 1 product    


# run server

if __name__ == "__main__":
    app.run(debug=True)