import json
from tests import BaseTests


class TestRegisterUserAPI(BaseTests):
    def setUp(self):
        super(TestRegisterUserAPI, self).setUp()

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
            "/api/v1/auth/register", data=dict(email='testor@example.com', password="sq33r"))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "password must have a minimum of 6 characters")
        self.assertEqual(data["status"], "failure")


class TestLogin(BaseTests):
    def setUp(self):
        super(TestLogin, self).setUp()

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


class TestResetPassword(BaseTests):
    def setUp(self):
        super(TestResetPassword, self).setUp()

    def test_reset_password_is_successful_for_an_existing_email(self):
        # Register a User
        resp = self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "user with email 'testor@example.com' has been registered")
        self.assertEqual(data["status"], "success")

        # reset password for `testor@example.com`
        # any password even if it is the original password,
        # once used should be able to invoke the password reset
        resp = self.test_client.post("/api/v1/auth/reset-password",
                                     data={'password': '!0ctoPus', 'confirm password': '!0ctoPus',
                                           'email': 'testor@example.com'})
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "success")
        self.assertEqual(
            data["message"], "password reset successful for 'testor@example.com'")

    def test_reset_password_fails_if_email_and_hence_user_is_non_existent(self):
        resp = self.test_client.post("/api/v1/auth/reset-password",
                                     data={'password': '!0ctoPus', 'confirm password': '!0ctoPus',
                                           'email': 'testor@example.com'})
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], 'user with email `testor@example.com` not found!')

    def test_reset_password_fails_if_the_given_passwords_do_not_match(self):
        resp = self.test_client.post("/api/v1/auth/reset-password",
                                     data={'password': '!0ctoPuS', 'confirm password': '!0ctoPus',
                                           'email': 'testor@example.com'})
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(data["message"], "the given passwords don't match")

    def test_reset_password_fails_if_password_has_less_than_8_characters_or_has_more_but_poorly_formatted(self):
        resp = self.test_client.post("/api/v1/auth/reset-password",
                                     data={'password': 'ten0R', 'confirm password': 'ten0R',
                                           'email': 'testor@example.com'})
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "password must have a minimum of 6 characters")

    def test_reset_password_fails_if_none_or_one_of_the_fields_are_not_given(self):
        # reset password for `testor@example.com`
        resp = self.test_client.post("/api/v1/auth/reset-password")
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "the fields: email, password, and 'confirm password' are required")
