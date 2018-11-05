[![Build Status](https://travis-ci.org/Paulstar200/Store-Manager-API-V2.svg?branch=bg-tests-fix-161618639)](https://travis-ci.org/Paulstar200/Store-Manager-API-V2)
[![Coverage Status](https://coveralls.io/repos/github/Paulstar200/Store-Manager-API-V2/badge.svg)](https://coveralls.io/github/Paulstar200/Store-Manager-API-V2)


# Store-Manager-API-V2

Store Manager is a web application that helps store owners manage sales and product inventory records. This application is meant for use in a single store.


# HEROKU LINK
https://storemanagerapi2.herokuapp.com


# DOCUMENTATION LINK
https://storemanagerapiv22.docs.apiary.io/#



# PIVOTAL TRACKER STORIES LINK
https://www.pivotaltracker.com/n/projects/2203237



# API DESIGN

The api is constructed using python flask and flask restful

Testing is done using unittest

Test coverage is done using `pytest-cov`


# Installation and Running the app

Clone the repo to your local machine.

Navigate to the project directory.

Install your virtual environment by doing `pip install virtualenv`.

Activate the virtual environment on mac by `$ source env\bin\activate`

Activate the virtual environment on windows by `env/scripts/activate`

Install the dependencies needed by doing `$ pip install -r requirements.txt`

Then setup the app in the terminal `$ export FLASK_APP=run.py`

Run using `python run.py`

open your localhost

open in Postman


# TESTING THE APP

Test the endpoints using Postman

Download [Postman](https://www.getpostman.com/)

Copy the link http://localhost/ into postman if running on your machine locally.

If using the heroku link, copy the link into postman.

Add endpoints as defined in the [documentation](https://storemanagerapiv22.docs.apiary.io/#)


# FEATURES

Store attendant can search and add products to buyer’s cart.

Store attendant can see his/her sale records but can’t modify them.

App should show available products, quantity and price.

Store owner can see sales and can filter by attendants.

Store owner can add, modify and delete products.

Store owner can give admin rights to a store attendant.


# EndPoint Functionality
Method | URL | DESCRIPTION
-------|-----|------------
GET /products| https://storemanagerapi2.herokuapp.com/api/v2/products | Fetch all products
GET /products/productId |https://storemanagerapi2.herokuapp.com/api/v2/products/<int: productId>| Fetch a single product record
GET /sales |https://storemanagerapi2.herokuapp.com/api/v2/sales|Fetch all sale records Get all sale records.
GET /sales/saleId | https://storemanagerapi2.herokuapp.com/api/v2/sales/<int: salesId> | Fetch a single sale record
POST /products| https://storemanagerapi2.herokuapp.com/api/v2/products | Create a product
POST /sales | https://storemanagerapi2.herokuapp.com/api/v2/sales | Create a sale order
POST /auth/login | https://storemanagerapi2.herokuapp.com/api/v2/auth/login | Log in a user
POST /auth/signup | https://storemanagerapi2.herokuapp.com/api/v2/auth/signup | Register a user
POST /auth/logout | https://storemanagerapi2.herokuapp.com/api/v2/auth/logout | Log out a user


