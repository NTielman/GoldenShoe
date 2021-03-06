import peewee
from flask import flash
from playhouse.shortcuts import model_to_dict
from models import User, Product, ProductUnit, Transaction, Review


def create_user(user_name, user_full_name, user_address, user_avatar, user_password):
    '''adds a user to database'''
    try:
        return User.create(
            username=user_name, full_name=user_full_name, address=user_address, avatar_url=user_avatar, password=user_password
        )
    except peewee.PeeweeException:
        return False


def get_user(user_name):
    '''finds and returns a user dictionary from database'''
    try:
        user = User.get(User.username == user_name)
        return model_to_dict(user)
    except peewee.DoesNotExist:
        return False


def get_user_password(user_name):
    '''finds a username and returns a user password from database'''
    try:
        user = User.get(User.username == user_name)
        return user.password
    except peewee.DoesNotExist:
        return False


def create_review(buyer_id, product_id, rating, description, image1, image2, image3):
    '''adds a product review to database'''
    try:
        return Review.create(
            buyer=User.get_by_id(buyer_id), product=Product.get_by_id(product_id), rating=rating, text_body=description, review_image1=image1, review_image2=image2, review_image3=image3
        )
    except peewee.PeeweeException:
        return False


def remove_review(user_id, review_id):
    '''removes a review from database'''
    try:
        user = User.get_by_id(user_id)
        review = Review.get_by_id(review_id)

        # ensure user deleting review is it's author
        if user == review.buyer:
            review_deleted = review.delete_instance()
            return review_deleted
        else:
            return False
    except peewee.IntegrityError:
        flash("Could not remove your review.", 'danger')
        return False


def get_product_base(product_id):
    '''finds and returns a base product dictionary from database'''
    try:
        product = Product.get_by_id(product_id)
        return model_to_dict(product, backrefs=True)
    except peewee.DoesNotExist:
        return False


def get_default_product(base_product_id):
    '''returns first product variant in stock'''
    try:
        base_product = Product.get_by_id(base_product_id)
        default_variant = ProductUnit.get(ProductUnit.prod_parent == base_product, ProductUnit.qty > 0)
        return model_to_dict(default_variant, backrefs=True)
    except peewee.DoesNotExist:
        return False


def get_product_unit(product_id):
    '''finds and returns a specific product variant from database'''
    try:
        product = ProductUnit.get_by_id(product_id)
        return model_to_dict(product, backrefs=True)
    except peewee.DoesNotExist:
        return False


def get_default_product_images(product_id):
    '''returns a list of product_images if any'''
    try:
        default_product = ProductUnit.get_by_id(product_id)
        images = [image.image_url for image in default_product.images]
        return images
    except peewee.DoesNotExist:
        return False


def get_product_sizes(product_id):
    '''returns a list of product sizes if any'''
    try:
        product = Product.get_by_id(product_id)
        product_variants = product.variants
        sizes = list(set(prod.size.size_value for prod in product_variants))
        return sizes
    except peewee.PeeweeException:
        return False


def get_product_colours(product_id):
    '''returns a list of product colours if any'''
    try:
        product = Product.get_by_id(product_id)
        product_variants = product.variants
        colours = list(set(prod.colour.colour_value for prod in product_variants))
        return colours
    except peewee.PeeweeException:
        return False


def get_product_reviews(product_id):
    '''returns a list of product reviews if any'''
    try:
        product = Product.get_by_id(product_id)
        reviews = [model_to_dict(review) for review in product.reviews]
        return reviews
    except peewee.PeeweeException:
        return False


def get_products():
    '''returns list of products in database'''
    query = (Product
             .select())
    products = [model_to_dict(product) for product in query]
    return products


def checkout(buyer_id, cart):
    '''adds purchase info to transactions database'''
    try:
        buyer = User.get_by_id(buyer_id)
        for item in cart:
            quantity = item['quantity']
            product = ProductUnit.get_by_id(item['id'])
            product_title = product.prod_parent.title

            if product.qty > quantity:
                Transaction.create(buyer=buyer, product=product, qty=quantity, product_thumb_url=product.thumbnail,
                                   prod_title=product_title, buyer_name=buyer.username)
                product.qty -= quantity
                product.save()
            else:
                flash(f"Could not order '{product_title}'. Not enough in stock", 'danger')
        return True
    except peewee.PeeweeException:
        return False