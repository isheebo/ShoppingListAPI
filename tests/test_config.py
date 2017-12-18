import unittest
import os
from app import create_app


class TestTestingConfiguration(unittest.TestCase):
    def setUp(self):
        self.test_app = create_app("testing")

    def test_app_is_created_with_right_configuration(self):
        self.assertTrue(self.test_app.config['DEBUG'])
        self.assertTrue(self.test_app.config['TESTING'])
        self.assertEqual(
            self.test_app.config['AUTH_EXPIRY_TIME_IN_SECONDS'], 3)
        self.assertFalse(
            self.test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])


class TestDevelopmentConfiguration(unittest.TestCase):
    def setUp(self):
        self.test_app = create_app()

    def test_app_is_created_with_development_configuration(self):
        self.assertFalse(self.test_app.config['TESTING'])
        self.assertTrue(self.test_app.config['DEBUG'])
        self.assertFalse(
            self.test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertEqual(
            self.test_app.config['AUTH_EXPIRY_TIME_IN_SECONDS'], 86400)


class TestProductionConfiguration(unittest.TestCase):
    def setUp(self):
        self.test_app = create_app("production")

    def test_app_is_created_with_production_configuration(self):
        self.assertFalse(self.test_app.config['DEBUG'])
        self.assertFalse(self.test_app.config['TESTING'])
        self.assertFalse(
            self.test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertEqual(
            self.test_app.config['AUTH_EXPIRY_TIME_IN_SECONDS'], 86400)
        self.assertIsNone(
            self.test_app.config['SQLALCHEMY_DATABASE_URI'])
        self.assertEqual(self.test_app.config['SQLALCHEMY_DATABASE_URI'],
                         os.getenv('DATABASE_URL'))
