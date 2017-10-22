import unittest
from app import create_app, db


class BaseTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.test_client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.user_data = dict(email="testor@example.com", password="!0ctoPus")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
