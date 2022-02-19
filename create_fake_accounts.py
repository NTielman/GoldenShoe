from models import create_tables
from helpers import verify_signup
from admin_queries import add_product_to_catalog, add_images_to_product, add_variant_to_catalog

##################################### admins ##############################################
# possible to use these admin details to log in, or create your own account
admin = {
    "full_name": 'Ad Min Addams',
    "username": 'TheAdminFamily',
    "password": 'w3dnesd@y',
}


##################################### users ##############################################
# possible to use any of these user details to log in, or create your own account

yuki = {
    "full_name": 'Yukine Masashi',
    "username": 'Yukiyuki_UwU',
    "password": 'BTSistheBest',
    "address": 'San Fransokyo 1234',
    "avatar_url": '../static/images/users/yuki.webp'
}

sam = {
    "full_name": 'Samantha Addams',
    "username": 'TheAddamsFamily',
    "password": 'sam.dams26',
    "address": 'The middle of nowhere 43',
    "avatar_url": '../static/images/users/sam.webp'
}

alaska = {
    "full_name": 'Alaska Jones',
    "username": 'The.Lion.Queen',
    "password": 'RickIsA-Morty',
    "address": 'Brooklyntown 168',
    "avatar_url": '../static/images/users/aska.webp'
}


##################################### product images ##############################################
# 

white_sneakers = [
                '../static/images/sneakers/sam-sneak1.webp',
                '../static/images/sneakers/sam-sneak2.webp',
                '../static/images/sneakers/sam-sneak3.webp',
                '../static/images/sneakers/sam-sneak4.webp',
                '../static/images/sneakers/sam-sneak5.webp',
                '../static/images/sneakers/sam-sneak6.webp'
                ]

white_heels = [
                '../static/images/heels/heels-white1.webp',
                '../static/images/heels/heels-white2.webp',
                '../static/images/heels/heels-white3.webp',
                '../static/images/heels/heels-white4.webp'
                ]

red_heels = [
                '../static/images/heels/heels-red1.webp',
                '../static/images/heels/heels-red2.webp',
                '../static/images/heels/heels-red3.webp'
                ]

black_heels = [
                '../static/images/heels/heels-black1.webp',
                '../static/images/heels/heels-black2.webp',
                '../static/images/heels/heels-black3.webp'
                ]

oxford_black = [
                '../static/images/oxford-shoes/oxford-black1.webp',
                '../static/images/oxford-shoes/oxford-black2.webp',
                '../static/images/oxford-shoes/oxford-black3.webp',
]

oxford_brown = [
                '../static/images/oxford-shoes/oxford-brown1.webp',
                '../static/images/oxford-shoes/oxford-brown2.webp',
                '../static/images/oxford-shoes/oxford-brown3.webp',
]


##################################### products ##############################################
# possible to edit, modify and update any of these products, or create your own

helen_heels = {
    'title': 'Helen Heels',
    'description': 'Some gorgeous heels. Perfect for a night out or a stroll through the city',
    'variants': [
        {
            'price_in_cents': 2090,
            'qty': 14,
            'size': 38,
            'colour': 'white',
            'images': white_heels
        }, 
        {
            'price_in_cents': 3000,
            'qty': 8,
            'size': 42,
            'colour': 'white',
            'images': white_heels
        }, 
        {
            'price_in_cents': 2090,
            'qty': 6,
            'size': 38,
            'colour': 'red',
            'images': red_heels
        }, 
        {
            'price_in_cents': 3000,
            'qty': 16,
            'size': 42,
            'colour': 'red',
            'images': red_heels
        }, 
        {
            'price_in_cents': 2050,
            'qty': 8,
            'size': 42,
            'colour': 'black',
            'images': black_heels
        },
        {
            'price_in_cents': 3000,
            'qty': 30,
            'size': 38,
            'colour': 'black',
            'images': black_heels
        }
    ]
}

sam_sneakers = {
    'title': 'Sam Sneakers',
    'description': 'Looking for some comfy sneakers to tackle your day with?! Look no further!',
    'variants': [
        {
            'price_in_cents': 5079,
            'qty': 56,
            'size': 38,
            'colour': 'white',
            'images': white_sneakers
        },
        {
            'price_in_cents': 6059,
            'qty': 20,
            'size': 40,
            'colour': 'white',
            'images': white_sneakers
        },
        {
            'price_in_cents': 8099,
            'qty': 32,
            'size': 42,
            'colour': 'white',
            'images': white_sneakers
        },
        {
            'price_in_cents': 10099,
            'qty': 17,
            'size': 46,
            'colour': 'white',
            'images': white_sneakers
        },
    ]
}

oxford_bold = {
    'title': 'Oxford Bold',
    'description': 'Simple, Classy, Bold',
    'variants': [
        {
            'price_in_cents': 8089,
            'qty': 74,
            'size': 38,
            'colour': 'black',
            'images': oxford_black
        },
        {
            'price_in_cents': 7050,
            'qty': 8,
            'size': 42,
            'colour': 'black',
            'images': oxford_black
        },
        {
            'price_in_cents': 9000,
            'qty': 30,
            'size': 48,
            'colour': 'black',
            'images': oxford_black
        },
        {
            'price_in_cents': 8089,
            'qty': 74,
            'size': 38,
            'colour': 'brown',
            'images': oxford_brown
        },
        {
            'price_in_cents': 7050,
            'qty': 8,
            'size': 42,
            'colour': 'brown',
            'images': oxford_brown
        },
        {
            'price_in_cents': 9000,
            'qty': 30,
            'size': 48,
            'colour': 'brown',
            'images': oxford_brown
        }
    ]
}


##################################### functions ##############################################
golden_users = [yuki, sam, alaska]
store_products = [helen_heels, sam_sneakers, oxford_bold]


def create_users(users):
    for user in users:
        verify_signup(user_name=user['username'], full_name=user['full_name'], address=user['address'], avatar_url=user['avatar_url'], password=user['password'])


def create_products(product_list):
    for product in product_list:
        prod_id = add_product_to_catalog(product)
        if prod_id:
            product_variants = product['variants']
            for variant in product_variants:
                variant_id = add_variant_to_catalog(parent_id=prod_id, product_info=variant)
                image_list = variant['images']
                add_images_to_product(variant_id, image_list)


def create_fake_db_accounts():
    '''creates 3 users and 3 products with variants 
    for testing site functionality with'''
    create_tables()
    create_users(golden_users)
    create_products(store_products)
