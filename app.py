from flask import render_template, redirect, url_for
from data import db, app, Customer, Order, Product, ProductOrder
from form import CustomerForm, OrderForm, ProductOrderForm, ProductForm, StatusForm, CustomerDelete, ProductDelete


@app.route('/')
def customer():
    try:
        customers = Customer.query.all()
    except:
        customers = []
    return render_template('customer.html', customers=customers)


@app.route("/product")
def product():
    try:
        products = Product.query.all()
    except:
        products = []
    return render_template("product.html", products=products)


@app.route("/orders")
def orders():
    try:
        orders = Order.query.all()[::-1]
    except:
        orders = []
    return render_template("orders.html", orders=orders)


@app.route("/new_customer", methods=["GET", "POST"])
def new_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(form.f_name.data, form.l_name.data, form.email.data)
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('customer'))
    return render_template("new_customer.html", form=form)


@app.route("/new_product", methods=["GET", "POST"])
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(form.name.data, form.price.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('product'))
    return render_template("new_product.html", form=form)


@app.route("/new_order", methods=["GET", "POST"])
def new_order():
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(form.customer.data.id, "1")
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('product_order', id=order.id))
    return render_template("new_order.html", form=form)


@app.route("/product_order/<int:id>", methods=["GET", "POST"])
def product_order(id):
    form = ProductOrderForm()
    if form.validate_on_submit():
        product_order = ProductOrder(product_id=form.product.data.id, order_id=id, quantity=form.quantity.data)
        db.session.add(product_order)
        db.session.commit()
        return redirect(url_for('product_order', id=id))
    return render_template("product_order.html", form=form)


@app.route("/status/<int:id>", methods=["GET", "POST"])
def status(id):
    user = Order.query.get(id)
    form = StatusForm()
    if form.validate_on_submit():
        user.status_id = form.status.data.id
        db.session.commit()
        return redirect(url_for('orders'))
    return render_template("status.html", form=form)


@app.route('/delete_order/<int:id>')
def delete_order(id):
    order = Order.query.get(id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('orders'))

@app.route("/delete_customers", methods=["GET", "POST"])
def delete_customers():
    form = CustomerDelete()
    if form.validate_on_submit():
        for customer in form.customer_del.data:
            orders = Order.query.all()
            for order in orders:
                if order.customer_id==customer.id:
                    db.session.delete(order)
                    db.session.delete(customer)
        db.session.commit()
        return redirect(url_for('customer'))
    return render_template("delete_customers.html", form=form)

@app.route("/delete_products", methods=["GET", "POST"])
def delete_products():
    form = ProductDelete()
    if form.validate_on_submit():
        for product in form.product_del.data:
            product_orders = ProductOrder.query.all()
            for product_order in product_orders:
                if product_order.product_id==product.id or product_order.product_id is None:
                    db.session.delete(product_order)
                    db.session.delete(product)
        db.session.commit()
        return redirect(url_for('product'))
    return render_template("delete_products.html", form=form)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
