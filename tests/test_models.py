import unittest
import time
from datetime import datetime
from app import create_app, db
from app.models import BaseModel, User, BlacklistToken, ShoppingList, Item


class TestModels(unittest.TestCase):
    def setUp(self):
        self.test_app = create_app("testing")
        self.app_context = self.test_app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.user = User("testing@example.com", "testers")

    def test_user_model_is_created_successfully(self):
        self.assertEqual(self.user.email, "testing@example.com")
        self.assertIsNone(self.user.id)
        # before a user is saved, date_added is None
        self.assertIsNone(self.user.date_added)
        self.assertTrue(self.user.save())
        self.assertIsNotNone(self.user.id)

    def test_user_can_validate_their_password(self):
        self.assertNotEqual(self.user.password, "testers")
        self.assertTrue(self.user.validate_password("testers"))
        self.assertFalse(self.user.validate_password("wrong-password"))

    def test_user_can_generate_authentication_token(self):
        self.assertTrue(self.user.save())
        user = User.query.filter_by(email=self.user.email).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.user.email)
        self.assertIsInstance(user.generate_token(user.id), bytes)

    def test_user_can_validate_an_authentication_token(self):
        self.assertTrue(self.user.save())
        user = User.query.filter_by(email=self.user.email).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.user.email)
        token = user.generate_token(user.id)
        self.assertIsInstance(token, bytes)
        user_id, err = user.verify_token(token)
        self.assertEqual(user_id, user.id)
        self.assertIsNone(err)

    def test_token_verification_fails_if_the_token_is_already_blacklisted(self):
        self.assertTrue(self.user.save())
        user = User.query.filter_by(email=self.user.email).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.user.email)
        token = user.generate_token(user.id)   # generating the token
        self.assertIsInstance(token, bytes)

        # add the token to the BlacklistToken
        BlacklistToken(str(token)).save()
        user_id, err = user.verify_token(token)
        self.assertIsNotNone(err)
        self.assertEqual(err, 'token has already expired: please re-login')
        self.assertIsNone(user_id)

    def test_token_is_successfully_blacklisted(self):
        self.assertTrue(self.user.save())
        user = User.query.filter_by(email=self.user.email).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.user.email)
        token = user.generate_token(user.id)   # generating the token
        self.assertIsInstance(token, bytes)

        # add the token to the BlacklistToken
        blacklist = BlacklistToken(str(token))
        blacklist.save()
        self.assertTrue(blacklist.is_blacklisted(str(token)))

    def test_shoppinglist_is_created_successfully(self):
        self.assertTrue(self.user.save())
        user = User.query.filter_by(email=self.user.email).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.user.email)
        shoppinglist = ShoppingList(user.id, "groceries")
        self.assertEqual(shoppinglist.name, "groceries")
        # until the shoppinglist is saved, its ID is None
        self.assertIsNone(shoppinglist.id)
        shoppinglist.save()
        queried_list = ShoppingList.query.filter_by(name="groceries").first()
        self.assertEqual(queried_list.name, shoppinglist.name)
        self.assertIsNotNone(shoppinglist.id)
        self.assertEqual(shoppinglist.user_id, user.id)

    def test_an_item_is_created_successfully(self):
        self.assertTrue(self.user.save())
        user = User.query.filter_by(email=self.user.email).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.user.email)
        shoppinglist = ShoppingList(user.id, "groceries")
        self.assertEqual(shoppinglist.name, "groceries")
        # until the shoppinglist is saved, its ID is None
        self.assertIsNone(shoppinglist.id)
        shoppinglist.save()
        queried_list = ShoppingList.query.filter_by(name="groceries").first()
        self.assertEqual(queried_list.name, shoppinglist.name)
        self.assertIsNotNone(shoppinglist.id)
        self.assertEqual(shoppinglist.user_id, user.id)
        item = Item(shoppinglist.id, "cabbages", "2", "5,000/=")
        self.assertIsNotNone(item)
        self.assertFalse(item.has_been_bought)
        self.assertIsNone(item.id)
        self.assertEqual(item.name, "cabbages")
        self.assertEqual(item.price, "5,000/=")
        self.assertEqual(item.quantity, "2")
        self.assertEqual(item.shoppinglist_id, shoppinglist.id)
        item.save()
        self.assertIsNotNone(item.id)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
