[![Build Status](https://travis-ci.org/isheebo/ShoppingListAPI.svg?branch=master)](https://travis-ci.org/isheebo/ShoppingListAPI)

# ShoppingList API
This project was done so as to improve on the code readability and test coverage of [ShoppingListerAPI](https://github.com/isheebo/shoppinglisterapi).

The ShoppingList API is a simple REST API built with Python and the Flask web application framework.

It consists of the following features:-
* Register a new user
* Login a user
* Logout a logged in user
* Reset password for a registered user
* Add shoppinglists/items
* Edit shoppinglists/items
* Delete shoppinglists/items

## API Endpoints

| Type | API EndPoint | Public Access | Usage |
| --- | --- | --- | --- |
| POST | `/api/v1/auth/register` | TRUE | Register a new user: requires an email and a password |
| POST | `/api/v1/auth/login` | TRUE | Log in a registered user using their email and password |
| POST | `/api/v1/auth/logout` | TRUE | Use a generated authentication token to logout a user|
| POST | `/api/v1/auth/reset-password` | TRUE | Change the password for a registered user |
| POST | `/api/v1/shoppinglists` | FALSE | Add a shopping list to a logged in user account |
| GET | `/api/v1/shoppinglists` | FALSE | View all shopping lists associated with a user account |
| GET | `/api/v1/shoppinglists/<id>` | FALSE | View the details of a shopping list specified by \<id\> |
| PUT | `/api/v1/shoppinglists/<id>` | FALSE | Edit the attributes of a shopping list using its \<id\>|
| DELETE | `/api/v1/shoppinglists/<id>` | FALSE | Deletes shopping list with \<id\>|
| POST | `/api/v1/shoppinglists/<id>/items/` | FALSE | Add item to the shopping list with that \<id\>|
| GET  |  `/api/v1/shoppinglists/<id>/items/` | FALSE | View all items in the shopping list with that \<id\>|
| PUT | `/api/v1/shoppinglists/<id>/items/<item_id>`| FALSE | Edit a shopping list item specified by \<item_id\> |
| DELETE | `/api/v1/shoppinglists/<id>/items/<item_id>` | FALSE | Delete an item from the specified shopping list |

## Getting Started
### Prerequisites
It is assumed that you have [Python 3.6](https://www.python.org) and [Git](https://git-scm.com) installed on your local environment. Check to ensure that both are added to Path.
```sh
$ git clone https://github.com/isheebo/ShoppingListAPI
$ cd ShoppingListAPI
$ pip install -r requirements.txt
```
### Database Setup
* [PostgreSQL](https://postgresql.org/download/) is utilised on the backend. If you have it installed, use the `pgAdmin` utility to create databases `ShoppingList` and `ShoppingListTest`. *(feel free to use the database names of your choice).*
* Change the `SQLALCHEMY_DATABASE_URL` in `config.py` to reflect the URLs of your databases.
* To check if you have properly set up your databases, run
```
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

## Running the Application
```
 $ python manage.py runserver
```

This will start at server running at address http://127.0.0.1:5000 . Append any endpoints to the end of this URL (e.g. http://127.0.0.1:5000/api/v1/auth/register) so as to test them. I would recommend you use [Postman](https://www.getpostman.com) for testing.

## Testing
From the root of the project, run
```
 $ nosetests -v --rednose --with-coverage --cover-package=app
```