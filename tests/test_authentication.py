import json
from tests import BaseTests


class TestRegisterUserAPI(BaseTests):
    def setUp(self):
        super(TestRegisterUserAPI, self).setUp()
        self.user_data = dict(email="testor@example.com", password="!0ctoPus")

    def test_user_is_successfully_registered_given_the_right_email_password(self):
        resp = self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "user with email 'testor@example.com' has been registered")
        self.assertEqual(data["status"], "success")

    def test_user_registration_fails_if_both_email_and_password_are_not_given(self):
        # no data attached on requests
        resp = self.test_client.post("/api/v1/auth/register")
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "you need to enter both the email and the password")
        self.assertEqual(data["status"], "failure")

    def test_user_registration_fails_if_email_is_of_invalid_format(self):
        resp = self.test_client.post(
            "/api/v1/auth/register", data=dict(email="a.b.c", password="Squ3@Ler"))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "invalid email format")
        self.assertEqual(data["status"], "failure")

    def test_user_registration_fails_if_user_with_email_already_exists(self):
        resp = self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "user with email 'testor@example.com' has been registered")
        self.assertEqual(data["status"], "success")

        resp = self.test_client.post(
            "/api/v1/auth/register", data=dict(email='testor@example.com', password="Squ3@Ler"))
        self.assertEqual(resp.status_code, 409)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "user with email 'testor@example.com' already exists")
        self.assertEqual(data["status"], "failure")

    def test_registration_fails_if_user_has_a_weak_password(self):
        resp = self.test_client.post(
            "/api/v1/auth/register", data=dict(email='testor@example.com', password="squ3@ler"))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "password must be 8 or more characters and should consist atleast one lower, uppercase "
            "letters, number and special character '(!@#$%^&*)'")
        self.assertEqual(data["status"], "failure")


class TestLogin(BaseTests):
    def setUp(self):
        super(TestLogin, self).setUp()
        self.user_data = dict(email="testor@example.com", password="!0ctoPus")

    def test_login_is_successful_for_existing_email_and_password(self):
        # Register a User
        resp = self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "user with email 'testor@example.com' has been registered")
        self.assertEqual(data["status"], "success")

        # Login a User

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "Login successful for 'testor@example.com'")
        self.assertEqual(data["status"], "success")

    def test_login_fails_if_password_is_incorrect(self):
        # Register a User
        resp = self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "user with email 'testor@example.com' has been registered")
        self.assertEqual(data["status"], "success")

        # Try logging in with a wrong password
        resp = self.test_client.post(
            "/api/v1/auth/login", data=dict(email='testor@example.com', password='1234567'))
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "Wrong password for the given email address")
        self.assertEqual(data["status"], "failure")

    def test_login_fails_if_email_is_unknown(self):
        # Try logging in with an unregistered email address
        resp = self.test_client.post(
            "/api/v1/auth/login", data=dict(email='testor@example.com', password='1234567'))
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "user with email 'testor@example.com' doesn't exist")
        self.assertEqual(data["status"], "failure")

    def test_login_fails_if_email_is_poorly_formatted(self):
        # Try logging in with an poorly formatted email address
        resp = self.test_client.post(
            "/api/v1/auth/login", data=dict(email='testor@e.c', password='1234567'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "invalid email format")
        self.assertEqual(data["status"], "failure")

    def test_login_fails_if_either_email_or_password_or_both_is_not_given(self):
        # Register a User
        resp = self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "user with email 'testor@example.com' has been registered")
        self.assertEqual(data["status"], "success")

        # Try logging in without providing email/password
        resp = self.test_client.post(
            "/api/v1/auth/login", data=dict(email='testor@example.com'))  # password not given
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "you need to enter both the email and the password"
        )
