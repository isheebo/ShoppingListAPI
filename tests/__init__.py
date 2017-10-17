import unittest
from app import create_app, db


class BaseTests(unittest.TestCase):
    def setUp(self):
        self.test_app = create_app("testing")
        self.app_context = self.test_app.request_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.test_app.request_context().pop()
