from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'orders.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column("Name", db.String)
    l_name = db.Column("Last name", db.String)
    email = db.Column("Email", db.String)

    def __init__(self, f_name, l_name, email):
        self.f_name = f_name
        self.l_name = l_name
        self.email = email


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column("Date", db.DateTime)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    customer = db.relationship("Customer")
    product_order = db.relationship("ProductOrder")
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"))
    status = db.relationship("Status")

    def __init__(self, customer_id, status_id):
        self.customer_id = customer_id
        self.date = datetime.now()
        self.status_id = status_id


class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name", db.String)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name", db.String)
    price = db.Column("Price", db.Float)

    def __init__(self, name, price):
        self.name = name
        self.price = price


class ProductOrder(db.Model):
    __tablename__ = "product_order"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    product = db.relationship("Product")
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    order = db.relationship("Order", overlaps="product_order")
    quantity = db.Column("Quantity", db.Integer)

    def __init__(self, product_id, order_id, quantity):
        self.product_id = product_id
        self.order_id = order_id
        self.quantity = quantity


db.create_all()
