import os
import user_queries
from cart import Cart
from helpers import verify_signin
from create_fake_accounts import create_fake_db_accounts
from flask import Flask, redirect, render_template, request, session, url_for, flash, abort


app = Flask(__name__)
app.secret_key = os.urandom(16)

# create_fake_db_accounts()  # comment out this line after db initialised


@app.route('/')
def frontpage():
    return render_template("index.html")


@app.route('/sign_in/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":

        # retrieve user info
        username = request.form["username"]
        password = request.form["password"]

        login_succesfull = verify_signin(username, password)

        if login_succesfull:
            # set session usser
            user = user_queries.get_user(username)
            session["user"] = user
            return redirect(url_for("frontpage"))
        else:
            return redirect(url_for('login'))

    else:  # request.method == "GET"
        if "user" in session:
            return redirect(url_for("frontpage"))
        return render_template('log_in.html')


@app.route('/sign_out/')
def logout():
    if "user" in session:
        session.pop("user", None)
        flash("You have been signed out", 'warning')
    return redirect(url_for("frontpage"))


@app.route('/product_page/<product_id>', methods=['GET', 'POST'])
def product_page(product_id):
    if request.method == "POST":  # product added to cart
        cart = Cart(session)

        # get product and quantity
        quantity = int(request.form["quantity"])
        # TODO pass produnit id in here
        user_cart = cart.add_product(
            product_id, quantity)  # returns a cart dict

        # update cart in session
        session['cart'] = user_cart
        session.modified = True
        flash("Item added to cart", 'success')

        return redirect(url_for("product_page", product_id=product_id, _method='GET'))
    else:  # request.method == "GET"
        product = user_queries.get_product_base(product_id)
        default_variant = user_queries.get_default_product(product_id)
        if product and default_variant:  
            sizes = user_queries.get_product_sizes(product_id)
            colours = user_queries.get_product_colours(product_id)
            reviews = user_queries.get_product_reviews(product_id)
            images = user_queries.get_default_product_images(default_variant['prod_id'])
            return render_template("product_page.html", product=product, default_product=default_variant, sizes=sizes, colours=colours, reviews=reviews, images=images)
        else:
            abort(404)

@app.route('/review_product/<product_id>', methods=['POST'])
def review_product(product_id):
    if "user" in session:
        buyer_id = session["user"]['user_id']
        rating = int(request.form["rating"])
        description = request.form["description"]
        image1 = request.form["img1"]
        image2 = request.form["img2"]
        image3 = request.form["img3"]
        review_created_succesfully = user_queries.create_review(buyer_id, product_id, rating, description, image1, image2, image3)

        if not review_created_succesfully:
            flash("Could not add your review, please try again later", 'danger')
        return redirect(url_for('product_page', product_id=product_id, _method='GET'))
    else:  # user must be logged in
        flash("you must be logged in to leave a review", 'warning')
        return redirect(url_for('login'))

@app.route('/view_cart/', methods=['GET', 'POST'])
def view_cart():
    if "user" in session:
        cart = Cart(session)

        if request.method == "POST":  # if user has checked out cart items
            buyer_id = session["user"]['user_id']
            order_placed_succesfully = user_queries.checkout(buyer_id, cart)

            if order_placed_succesfully:
                session.pop("cart", None)
                return redirect(url_for('success'))
            else:
                flash("Something went wrong, could not place your order", 'danger')
                return redirect(url_for('view_cart'))

        else:  # request.method == "GET"
            remove_cart_item = request.args.get(
                'remove_from_cart', '')  # stores a product_id
            update_item_qty = request.args.get(
                'change_quantity', '')  # stores a product_id
            quantity = int(request.args.get('quantity', 0))

            if remove_cart_item:
                user_cart = cart.remove_product(remove_cart_item)
                session['cart'] = user_cart
                session.modified = True
                return redirect(url_for('view_cart'))

            if update_item_qty:
                user_cart = cart.add_product(update_item_qty, quantity)
                session['cart'] = user_cart
                session.modified = True
                return redirect(url_for('view_cart'))

            return render_template('cart.html', cart=cart)
    else:  # user must be logged in
        flash("you must be logged in to view your cart", 'warning')
        return redirect(url_for('login'))


@app.route('/checkout/success/')
def success():
    return render_template('success.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
