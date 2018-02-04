[![Build Status](https://travis-ci.org/isheebo/ShoppingListAPI.svg?branch=master)](https://travis-ci.org/isheebo/ShoppingListAPI)
[![Coverage Status](https://coveralls.io/repos/github/isheebo/ShoppingListAPI/badge.svg?branch=master)](https://coveralls.io/github/isheebo/ShoppingListAPI?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a6c6f4fde53b4be18654832b16905249)](https://www.codacy.com/app/isheebo/ShoppingListAPI?utm_source=github.com&utm_medium=referral&utm_content=isheebo/ShoppingListAPI&utm_campaign=Badge_Grade)

# ShoppingList API

This project is hosted on Heroku. It can be accessed here
https://shoppinglistapi1.herokuapp.com

The ShoppingList API is a simple REST API built with Python and the Flask web
application framework.

It consists of the following features:-

* Register a new user
* Login a user
* Logout a logged in user
* Reset password for a registered user
* Add shoppinglists/items
* Edit shoppinglists/items
* Delete shoppinglists/items

## API Endpoints

| Type   | API EndPoint                                 | Public Access | Usage                                                                      |
| ------ | -------------------------------------------- | ------------- | -------------------------------------------------------------------------- |
| POST   | `/api/v1/auth/register`                      | TRUE          | Register a new user: requires an email and a password                      |
| POST   | `/api/v1/auth/login`                         | TRUE          | Log in a registered user using their email and password                    |
| POST   | `/api/v1/auth/logout`                        | TRUE          | Use a generated authentication token to logout a user                      |
| POST   | `/api/v1/auth/reset-password`                | TRUE          | Change the password for a registered user                                  |
| POST   | `/api/v1/shoppinglists`                      | FALSE         | Add a shopping list to a logged in user account                            |
| GET    | `/api/v1/shoppinglists`                      | FALSE         | View all shopping lists associated with a user account                     |
| GET    | `/api/v1/shoppinglists/<id>`                 | FALSE         | View the details of a shopping list specified by \<id\>                    |
| PUT    | `/api/v1/shoppinglists/<id>`                 | FALSE         | Edit the attributes of a shopping list using its \<id\>                    |
| DELETE | `/api/v1/shoppinglists/<id>`                 | FALSE         | Deletes shopping list with \<id\>                                          |
| POST   | `/api/v1/shoppinglists/<id>/items/`          | FALSE         | Add item to the shopping list with that \<id\>                             |
| GET    | `/api/v1/shoppinglists/<id>/items/`          | FALSE         | View all items in the shopping list with that \<id\>                       |
| GET    | `/api/v1/shoppinglists/<id>/items/<item_id>` | FALSE         | View one item on a shoppinglist with its ID \<id\> and item ID \<item_id\> |  |
| PUT    | `/api/v1/shoppinglists/<id>/items/<item_id>` | FALSE         | Edit a shopping list item specified by \<item_id\>                         |
| DELETE | `/api/v1/shoppinglists/<id>/items/<item_id>` | FALSE         | Delete an item from the specified shopping list                            |

## Getting Started

### Prerequisites

It is assumed that you have [Python 3.6](https://www.python.org) and
[Git](https://git-scm.com) installed on your local environment. Check to ensure
that both are added to Path.

Start by cloning this repository. This will create a directory `ShoppingListAPI`
on your local machine.

```sh
$ git clone https://github.com/isheebo/ShoppingListAPI
```

In this directory/folder, You would need to create a Python virtual environment and activate it.

If the virtualenv package is not installed globally, run `pip install virtualenv` from the commandline. Then, a
virtual environment with name `virtualenv` can be created by running

```sh
$ virtualenv -p python3 ./virtualenv
```

On Windows, create the virtual environment as indicated below

```sh
$ virtualenv --python=<path to your python 3 executable> ./virtualenv
```

where by the `virtualenv` is the virtual environment folder created in the
`ShoppingListAPI` directory.

Then you can activate the virtual environment and install the requirements as shown below:-

On Unix _(MacOS X, Linux and BSD)_ based systems,

```sh
$ source virtualenv/bin/activate
$ pip3 install -r requirements.txt
```

On Windows,

```sh
$ cd virtualenv/scripts
$ activate
$ cd ..
$ cd ..
$ pip install -r requirements.txt
```

**Note:**

* To install the requirements using _`pip`_ as mentioned above, make sure
  you are in the root folder _(ShoppingListAPI folder)_. That is, where the file `requirements.txt` is located in
  the directory tree.
* on MacOSx, Linux & BSD, `pip3` should be used instead of `pip`.

### Database Setup

* [PostgreSQL](https://www.postgresql.org) is utilised on the backend. If you
  are unfamiliar with the commandline, I would recommend you install your
  PostgresSQL from the [PostgresSQL](https://www.postgresql.org/download/)
  website. This option comes with the `pgAdmin` utility _(or Postgres.app for MacOs X)_ which may be easier to
  interact with when compared to the terminal or the HomeBrew installation.

* If you have PostgresSQL installed, create databases `ShoppingList` and
  `ShoppingListTest`. _(if you use other database names, change the
  `SQLALCHEMY_DATABASE_URL` in `config.py` to reflect the URLs of your
  databases.)_

* Create a file `settings.py` in the root of your project _(at the same level as
  `manage.py` file)_.

* In the `settings.py` file, create DATABASE_URL and TEST_DATABASE_URL variables
  and assign the database URL and the test database URL respectively to the
  created variables.

* To check if you have properly configured your databases, run

```
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

## Running the Application

```
 $ python3 manage.py runserver
```

This will start at server running at address http://127.0.0.1:5000 . Append any
endpoints to the end of this URL (e.g.
http://127.0.0.1:5000/api/v1/auth/register) so as to test them. I would
recommend you use [Postman](https://www.getpostman.com) for testing.

## Testing

To run the tests of the project, use

```
 $ nosetests -v --rednose --with-coverage --cover-package=app
```
