from datetime import datetime, timedelta

import psycopg2
import jwt
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Boolean
from flask import current_app
from flask_bcrypt import Bcrypt

from app import db


class BaseModel:
    """
    BaseModel is an abstract class consisting of methods
    that are common amongst all the models. """

    def save(self):
        has_been_saved = False
        try:
            db.session.add(self)
            db.session.commit()
            has_been_saved = True
        except (RuntimeError, psycopg2.Error):
            db.session.rollback()
        return has_been_saved

    def delete(self):
        """ delete is a utility method that deletes an instance of
        a model from a database"""
        is_deleted = False
        try:
            db.session.delete(self)
            db.session.commit()
            is_deleted = True
        except (RuntimeError, psycopg2.Error):
            db.session.rollback()
        return is_deleted


class User(db.Model, BaseModel):
    """Model for a shopping list app user"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    date_added = Column(DateTime, default=datetime.now())
    shoppinglists = db.relationship(
        'ShoppingList', order_by='ShoppingList.id', cascade='all, delete-orphan')

    def __init__(self, email, password):
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode('utf-8')

    def validate_password(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    @staticmethod
    def generate_token(user_id):
        try:
            payload = dict(iat=datetime.utcnow(),
                           exp=(datetime.utcnow() +
                                timedelta(seconds=current_app.config['AUTH_EXPIRY_TIME_IN_SECONDS'])),
                           sub=user_id)
            return jwt.encode(payload=payload, key=current_app.config['SECRET_KEY'], algorithm='HS256')
        except (NotImplementedError, KeyError):
            pass

    @staticmethod
    def verify_token(token):
        try:
            if BlacklistToken.is_blacklisted(token):
                return None, "token has already expired: please re-login"
            payload = jwt.decode(
                token, key=current_app.config['SECRET_KEY'], algorithms=['HS256', 'HS512'])
            return payload['sub'], None

        except jwt.DecodeError:
            return None, "the given token is invalid. please re-login"

        except jwt.ExpiredSignatureError:
            return None, "the token has expired: please re-login"


class BlacklistToken(db.Model, BaseModel):
    """BlacklistToken stores any previously issued
    token that have expired and therefore ceased from being used"""

    __tablename__ = 'blacklisted_tokens'
    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True, nullable=False)
    # token is unique such that once a token has been blacklisted, it can't be blacklisted again

    def __init__(self, token):
        self.token = token

    @staticmethod
    def is_blacklisted(token):
        result = BlacklistToken.query.filter_by(token=str(token)).first()
        if result:
            return True
        return False


class ShoppingList(db.Model, BaseModel):
    __tablename__ = "shoppinglists"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id))

    name = Column(String, nullable=False)
    notify_date = Column(Date, nullable=False)
    items = db.relationship('Item', order_by="Item.id",
                            cascade="all, delete-orphan")

    date_created = Column(DateTime, default=datetime.now())
    date_modified = Column(DateTime, default=datetime.now())

    def __init__(self, user_id, name, notify_date):
        self.user_id = user_id
        self.name = name
        self.notify_date = datetime.strptime(notify_date, "%Y-%m-%d")


class Item(db.Model, BaseModel):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    shoppinglist_id = Column(Integer, ForeignKey(ShoppingList.id))
    name = Column(String)
    price = Column(String)
    quantity = Column(String)
    has_been_bought = Column(Boolean, default=False)

    date_added = Column(DateTime, default=datetime.now())
    date_modified = Column(DateTime, default=datetime.now())

    def __init__(self, list_id, name, quantity, price, status=False):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.shoppinglist_id = list_id
        self.has_been_bought = status
