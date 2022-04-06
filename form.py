from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField
from wtforms.validators import DataRequired, Email
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms_sqlalchemy.fields import QuerySelectField
from data import Customer, Product, Status


class CustomerForm(FlaskForm):
    f_name = StringField('Name', [DataRequired()])
    l_name = StringField('Last name', [DataRequired()])
    email = StringField('Email', [Email(message=('Invalid address')), DataRequired()],
                        render_kw={"placeholder": "email@address.com"})
    submit = SubmitField('Submit')


class ProductForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    price = FloatField('Price', [DataRequired()])
    submit = SubmitField('Submit')


def customer_query():
    return Customer.query


class OrderForm(FlaskForm):
    customer = QuerySelectField(query_factory=customer_query, get_label="f_name", get_pk=lambda obj: str(obj))
    submit = SubmitField('Submit')


def status_query():
    return Status.query


class StatusForm(FlaskForm):
    status = QuerySelectField(query_factory=status_query, get_label="name", get_pk=lambda obj: str(obj))
    submit = SubmitField('Submit')


def product_query():
    return Product.query


class ProductOrderForm(FlaskForm):
    product = QuerySelectField(query_factory=product_query, get_label="name", get_pk=lambda obj: str(obj))
    quantity = IntegerField('Quantity', [DataRequired()])
    submit = SubmitField('Add')


class CustomerDelete(FlaskForm):
    customer_del = QuerySelectMultipleField("Please select...", query_factory=customer_query, get_label="f_name",
                                        get_pk=lambda obj: str(obj))
    submit = SubmitField('Delete')

class ProductDelete(FlaskForm):
    product_del = QuerySelectMultipleField("Please select...", query_factory=product_query, get_label="name",
                                        get_pk=lambda obj: str(obj))
    submit = SubmitField('Delete')