import peewee
from models import Product, ProductUnit, Image, Size, Colour


def add_product_to_catalog(product_info):
    '''creates and adds a product to database'''
    try:
        product = Product.create(title=product_info["title"], description=product_info['description'])
        return product.prod_id
    except peewee.PeeweeException:
        return False


def add_variant_to_catalog(parent_id, product_info):
    '''creates and adds a product variant'''
    try:
        product_variant = ProductUnit.create(prod_parent=Product.get_by_id(parent_id), qty=product_info['qty'], price_in_cents=product_info['price_in_cents'])
        if product_variant.prod_id:
            if product_info["size"]:
                product_variant.size , created = Size.get_or_create(size_value=product_info["size"])
            if product_info['colour']:
                product_variant.colour , created = Colour.get_or_create(colour_value=product_info['colour'])
        product_variant.save()
        return product_variant.prod_id
    except peewee.PeeweeException:
        return False


def add_images_to_product(product_id, image_list):
    '''adds list of images to a product variant'''
    product = ProductUnit.get_by_id(product_id)

    # set first image as product thumbnail
    product.thumbnail = image_list[0]
    product.save()

    for image_url in image_list:
        if image_url:  # if image field isn't empty
            prod_image , created = Image.get_or_create(image_url=image_url)
            prod_image.product.add(product)
            prod_image.save()