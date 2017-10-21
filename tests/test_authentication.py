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
        self.assertIsNotNone(data["token"])

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


class TestLogout(BaseTests):
    def setUp(self):
        super(TestLogout, self).setUp()
        self.user_data = dict(email="testor@example.com", password="Squ3@Ler")

    def test_logout_is_successful_for_a_logged_in_user(self):
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
        self.assertIsNotNone(data["token"])

        # Logout a user
        resp = self.test_client.post(
            "/api/v1/auth/logout", headers=dict(Authorization=f"Bearer {data['token']}"))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "success")
        self.assertEqual(
            data["message"], "Successfully logged out 'testor@example.com'")

    def test_logout_fails_if_authorization_header_is_not_provided(self):
        # Try Logging out without an Authorization header
        resp = self.test_client.post("/api/v1/auth/logout")
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], 'Authorization header must be set for a successful request')

    def test_logout_fails_if_authorization_header_is_poorly_formatted(self):
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
        self.assertIsNotNone(data["token"])

        # Try Logging out a user with a poorly formatted Authorization Header
        resp = self.test_client.post("/api/v1/auth/logout",  # right word should be 'Bearer'*
                                     headers=dict(Authorization=f"Bearers {data['token']}"))
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "Authentication Header is poorly formatted. The acceptable format is `Bearer <jwt_token>`")

    def test_logout_fails_if_token_has_expired_or_is_corrupted(self):
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
        self.assertIsNotNone(data["token"])

        invalid_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1MDg2MTExNjgs" + \
            "ImV4cCI6MTUwODYxNDc2OCwic3ViIjoyfQ.I_WBI93N3PRlAXOasnXJ5QY4Zg0ggvNXA4b2B2CQ9g0"

        # For an expired/blacklisted/invalid token but of right length
        resp = self.test_client.post("/api/v1/auth/logout",
                                     headers=dict(Authorization=f"Bearer {invalid_token}"))
        self.assertEqual(resp.status_code, 401)
        data = json.loads(resp.data)

        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], 'error in token: Signature verification failed')

        # for a token with an invalid/corrupted header
        resp = self.test_client.post("/api/v1/auth/logout",
                                     headers=dict(Authorization=f"Bearer {invalid_token[2:]}"))
        self.assertEqual(resp.status_code, 401)
        data = json.loads(resp.data)

        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "error in token: Invalid header string: 'utf-8' codec "
            "can't decode byte 0x97 in position 2: invalid start byte")

        # for a token with an invalid/corrupted payload
        resp = self.test_client.post("/api/v1/auth/logout",
                                     headers=dict(Authorization=f"Bearer {invalid_token[:41] + invalid_token[42:]}"))
        self.assertEqual(resp.status_code, 401)
        data = json.loads(resp.data)

        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "error in token: Invalid payload padding")

    def test_logout_fails_if_an_already_blacklisted_token_is_used(self):
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
        self.assertIsNotNone(data["token"])

        token = data['token']
        # Logout a user
        resp = self.test_client.post(
            "/api/v1/auth/logout", headers=dict(Authorization=f"Bearer {token}"))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "success")
        self.assertEqual(
            data["message"], "Successfully logged out 'testor@example.com'")

        # On first logout, the token is blacklisted, on the second, the logout should fail with an error.
        resp = self.test_client.post(
            "/api/v1/auth/logout", headers=dict(Authorization=f"Bearer {token}"))
        self.assertEqual(resp.status_code, 401)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], 'error in token: token has already expired')
