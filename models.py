from email.mime import image
from email.policy import default
import os
from random import choices
from peewee import *
from datetime import date

# Ensure database "goldenShoe.db" is created in current folder
full_path = os.path.realpath(__file__)
file_dir = os.path.dirname(full_path)
db_path = os.path.join(file_dir, 'goldenShoe.db')

db = SqliteDatabase(db_path, pragmas={'foreign_keys': 1})
# Pragmas ensure foreign-key constraints are enforced.

VARIANTS = (
    ('None', 'None'),
    ('Size', 'Size'),
    ('Color', 'Color'),
    ('Size-Color', 'Size-Color')
)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = AutoField()
    username = CharField(unique=True, max_length=100)
    password = CharField()
    full_name = CharField()
    address = CharField()
    avatar_url = CharField(null=True)

class Admin(BaseModel):
    admin_id = AutoField()
    username = CharField(unique=True, max_length=100)
    password = CharField()
    full_name = CharField()


class Product(BaseModel):
    prod_id = AutoField()
    title = CharField(max_length=100)
    description = TextField(null=True)
    has_variants = CharField(choices=VARIANTS, default='None')


class Size(BaseModel):
    size_id = AutoField()
    size_value = IntegerField(unique=True)


class Colour(BaseModel):
    colour_id = AutoField()
    colour_value = CharField(max_length=50, unique=True)


class ProductUnit(BaseModel):
    prod_id = AutoField()
    prod_parent = ForeignKeyField(Product, backref='variants', on_delete='CASCADE')
    size = ForeignKeyField(Size, backref='products', null=True, on_delete='CASCADE')
    colour = ForeignKeyField(Colour, backref='products', null=True, on_delete='CASCADE')
    thumbnail = CharField(null=True)
    qty = IntegerField(constraints=[Check('qty >= 0')])
    price_in_cents = IntegerField(constraints=[Check('price_in_cents >= 0')])


class Transaction(BaseModel):
    trans_id = AutoField()
    buyer = ForeignKeyField(User, backref='purchases',
                            on_delete='SET NULL', null=True)
    product = ForeignKeyField(
        ProductUnit, backref='orders', on_delete='SET NULL', null=True)
    qty = IntegerField(constraints=[Check('qty > 0')])
    date = DateField(default=date.today())
    # if product or user is modified or deleted from db we should still
    # be able to view some of their info in (existing) orders
    # by storing them as order details (below)
    product_thumb_url = CharField(null=True)
    prod_title = CharField(max_length=100)
    buyer_name = CharField(max_length=100)


class Review(BaseModel):
    review_id = AutoField()
    buyer = ForeignKeyField(User, backref='reviews',
                            on_delete='SET NULL', null=True)
    # if product or user is deleted from db we should still
    # be able to view product_review
    product = ForeignKeyField(
        Product, backref='reviews', on_delete='CASCADE', null=False)
    rating = IntegerField(constraints=[Check('rating > 0 '), Check('rating < 6')])
    date = DateField(default=date.today())
    text_body = TextField(null=True)
    # Allow users to add 3 images to review
    review_image1 = CharField(null=True)
    review_image2 = CharField(null=True)
    review_image3 = CharField(null=True)


class Image(BaseModel):
    img_id = AutoField()
    image_url = CharField(unique=True)
    product = ManyToManyField(ProductUnit, backref='images', on_delete='SET NULL')


ProductImage = Image.product.get_through_model()


def create_tables():
    with db:
        db.create_tables([User, Admin, Product, Size, Colour, ProductUnit, Transaction, Review, Image, ProductImage])
