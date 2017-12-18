import json
import time
from tests import BaseTests


class TestRegisterUserAPI(BaseTests):
    def test_user_is_successfully_registered_given_the_right_email_password(self):
        resp = self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"],
            "user with email 'testor@example.com' has been registered")
        self.assertEqual(data["status"], "success")

    def test_user_registration_fails_if_both_email_and_password_are_not_given(self):
        resp = self.test_client.post("/api/v1/auth/register")
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "you need to enter both the email and the password")
        self.assertEqual(data["status"], "failure")

    def test_user_registration_fails_if_email_is_of_invalid_format(self):
        resp = self.test_client.post(
            "/api/v1/auth/register",
            data=dict(email="a.b.c", password="Squ3@Ler"))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "invalid email format")
        self.assertEqual(data["status"], "failure")

    def test_user_registration_fails_if_user_with_email_already_exists(self):
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/register",
            data=dict(email='testor@example.com', password="Squ3@Ler"))
        self.assertEqual(resp.status_code, 409)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "user with email 'testor@example.com' already exists")
        self.assertEqual(data["status"], "failure")

    def test_registration_fails_if_user_has_a_weak_password(self):
        resp = self.test_client.post(
            "/api/v1/auth/register",
            data=dict(email='testor@example.com', password="sq33r"))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "password must have a minimum of 6 characters")
        self.assertEqual(data["status"], "failure")


class TestLogin(BaseTests):

    def test_login_is_successful_for_existing_email_and_password(self):
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "Login successful for 'testor@example.com'")
        self.assertEqual(data["status"], "success")
        self.assertIsNotNone(data["token"])

    def test_login_fails_if_password_is_incorrect(self):
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login",
            data=dict(email='testor@example.com', password='1234567'))
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "Wrong password for the given email address")
        self.assertEqual(data["status"], "failure")

    def test_login_fails_if_email_is_unknown(self):
        resp = self.test_client.post(
            "/api/v1/auth/login",
            data=dict(email='testor@example.com', password='1234567'))
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "user with email 'testor@example.com' doesn't exist")
        self.assertEqual(data["status"], "failure")

    def test_login_fails_if_email_is_poorly_formatted(self):
        resp = self.test_client.post(
            "/api/v1/auth/login",
            data=dict(email='testor@e.c', password='1234567'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "invalid email format")
        self.assertEqual(data["status"], "failure")

    def test_login_fails_if_either_email_or_password_or_both_are_not_given(self):
        resp = self.test_client.post(
            "/api/v1/auth/login",
            data=dict(email='testor@example.com'))  # password not given
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"],
            "you need to enter both the email and the password"
        )


class TestLogout(BaseTests):

    def test_logout_is_successful_for_a_logged_in_user(self):
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        resp = self.test_client.post(
            "/api/v1/auth/logout",
            headers=dict(Authorization=f"Bearer {data['token']}"))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "success")
        self.assertEqual(
            data["message"], "Successfully logged out 'testor@example.com'")

    def test_logout_fails_if_authorization_header_is_not_provided(self):
        resp = self.test_client.post("/api/v1/auth/logout")
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], 'Authorization header must be set for a successful request')

    def test_logout_fails_if_authorization_header_is_poorly_formatted(self):
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        resp = self.test_client.post(
            "/api/v1/auth/logout",
            headers=dict(Authorization=f"Bearers {data['token']}"))
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "Authentication Header is poorly formatted. "
                             "The acceptable format is `Bearer <jwt_token>`")

    def test_logout_fails_if_token_is_corrupted(self):
        invalid_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1MDg2MTExNjgs" + \
                        "ImV4cCI6MTUwODYxNDc2OCwic3ViIjoyfQ.I_WBI93N3PRlAXOasnXJ5QY4Zg0ggvNXA4b2B2CQ9g0"

        # For an invalid token but of right length
        resp = self.test_client.post(
            "/api/v1/auth/logout",
            headers=dict(Authorization=f"Bearer {invalid_token}"))
        self.assertEqual(resp.status_code, 401)
        data = json.loads(resp.data)

        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "the given token is invalid. please re-login")

        # for a token with an invalid/corrupted header
        resp = self.test_client.post(
            "/api/v1/auth/logout",
            headers=dict(Authorization=f"Bearer {invalid_token[2:]}"))
        self.assertEqual(resp.status_code, 401)
        data = json.loads(resp.data)

        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "the given token is invalid. please re-login")

        # for a token with an invalid/corrupted payload
        resp = self.test_client.post(
            "/api/v1/auth/logout",
            headers=dict(
                Authorization=f"Bearer {invalid_token[:41] + invalid_token[42:]}"))
        self.assertEqual(resp.status_code, 401)
        data = json.loads(resp.data)

        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "the given token is invalid. please re-login")

    def test_logout_fails_for_an_expired_auth_token(self):
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        # after 4 seconds in testing mode, the token will have expired
        time.sleep(4)
        resp = self.test_client.post(
            "/api/v1/auth/logout",
            headers=dict(Authorization=f"Bearer {data['token']}"))
        self.assertEqual(resp.status_code, 401)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(data["message"], "the token has expired: please re-login")

    def test_logout_fails_if_an_already_blacklisted_token_is_used(self):
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        token = data['token']

        self.test_client.post(
            "/api/v1/auth/logout",
            headers=dict(Authorization=f"Bearer {token}"))

        resp = self.test_client.post(
            "/api/v1/auth/logout",
            headers=dict(Authorization=f"Bearer {token}"))
        self.assertEqual(resp.status_code, 401)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], 'token has already expired: please re-login')


class TestResetPassword(BaseTests):
    def test_reset_password_is_successful_for_an_existing_user(self):
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        # reset-password should pass provided the new password
        #  is not similar to the old saved password
        token = data['token']
        resp = self.test_client.post(
            "/api/v1/auth/reset-password",
            headers=dict(Authorization=f"Bearer {token}"),
            data={'password': '0ctoPus', 'confirm password': '0ctoPus'})

        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.data)
        self.assertEqual(data["status"], "success")
        self.assertEqual(
            data["message"], "password reset successful for 'testor@example.com'")

    def test_reset_password_fails_if_new_password_is_similar_to_old_password(self):
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        # reset-password should pass provided the new password
        # is not similar to the old saved password
        token = data['token']
        resp = self.test_client.post(
            "/api/v1/auth/reset-password",
            headers=dict(Authorization=f"Bearer {token}"),
            data={'password': '!0ctoPus', 'confirm password': '!0ctoPus'}
        )

        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "Your new password should not be similar to your old password")

    def test_reset_password_fails_if_the_given_passwords_do_not_match(self):
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        token = data['token']

        resp = self.test_client.post(
            "/api/v1/auth/reset-password",
            headers=dict(Authorization=f"Bearer {token}"),
            data={'password': '!0ctoPus1', 'confirm password': '!0ctoPus'}
        )

        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(data["message"], "the given passwords don't match")

    def test_reset_password_fails_if_password_has_less_than_6_characters(self):
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        token = data['token']
        resp = self.test_client.post(
            "/api/v1/auth/reset-password",
            headers=dict(Authorization=f"Bearer {token}"),
            data={'password': 'ten0R', 'confirm password': 'ten0R',
                  'email': 'testor@example.com'})
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "password must have a minimum of 6 characters")

    def test_reset_password_fails_if_none_or_one_of_the_fields_are_not_given(self):
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        token = data['token']

        resp = self.test_client.post("/api/v1/auth/reset-password",
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "the fields 'password' and 'confirm password' are required")

    def test_reset_password_fails_for_no_authorization_header_specified(self):
        resp = self.test_client.post(
            "/api/v1/auth/reset-password",
            data={'password': 'ten0Rs', 'confirm password': 'ten0Rs',
                  'email': 'testor@example.com'})
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "Authorization header must be set for a successful request")

    def test_reset_password_fails_if_auth_header_specified_but_in_poor_format(self):
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        token = data['token']
        resp = self.test_client.post(
            "/api/v1/auth/reset-password",
            headers=dict(Authorization=f"Bearers {token}"),
            data={'password': 'ten0Rs', 'confirm password': 'ten0Rs',
                  'email': 'testor@example.com'})
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "Authentication Header is poorly formatted. "
                             "The acceptable format is `Bearer <jwt_token>`")
