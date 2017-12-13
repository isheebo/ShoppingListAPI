import json
from datetime import datetime
import time
from tests import BaseTests


class TestShoppingListAPI(BaseTests):
    def test_post_shopping_list_is_successful_if_all_requirements_are_given(self):
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

        # Add a shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {data["token"]}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

    def test_post_shoppinglist_fails_for_invalidly_formatted_notify_date(self):
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

        # Add a shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "201x-03-14"},
                                     headers=dict(Authorization=f'Bearer {data["token"]}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data['message'], "dates must be specified as strings but with integer values")

    def test_post_shoppinglist_fails_for_a_notify_date_with_year_before_today(self):
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

        request_data = {"name": "groceries", "notify date": "1000-03-14"}
        # Add a shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data=request_data,
                                     headers=dict(Authorization=f'Bearer {data["token"]}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data['message'], "The year {} already passed, please use "
                             "a valid year".format(request_data["notify date"].split("-")[0]))

    def test_post_shoppinglist_fails_for_a_notify_date_with_year_beyond_2100(self):
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

        request_data = {"name": "groceries", "notify date": "2110-03-14"}
        # Add a shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data=request_data,
                                     headers=dict(Authorization=f'Bearer {data["token"]}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data['message'], "By {}, you may be in afterlife, please consider years in "
                             "range (2017-2099)".format(request_data["notify date"].split("-")[0]),
            datetime.today().year)

    def test_post_shoppinglist_fails_for_a_notify_date_with_current_year_but_a_month_that_has_already_passed(self):
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

        request_data = {"name": "groceries", "notify date": "2017-03-14"}
        # Add a shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data=request_data,
                                     headers=dict(Authorization=f'Bearer {data["token"]}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data['message'], "Invalid date, March 2017 has already passed by")

    def test_post_fails_for_a_notify_date_with_current_year_and_month_but_date_that_has_already_passed(self):
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

        request_data = {"name": "groceries", "notify date": "2017-12-01"}
        # Add a shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data=request_data,
                                     headers=dict(Authorization=f'Bearer {data["token"]}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data['message'], "Use dates starting from {}".format(datetime.now().strftime("%d/%m/%Y")))

    def test_post_shopping_list_fails_if_token_has_already_expired(self):
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

        time.sleep(12)  # enough time for the token to expire in testing mode.

        # try adding a shoppinglist.
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {data["token"]}'))
        self.assertEqual(resp.status_code, 401)

        data = json.loads(resp.data)
        self.assertEqual(
            data['message'], "the token has expired: please re-login")

    def test_post_shopping_list_fails_if_no_authorization_header_is_specified(self):
        resp = self.test_client.post(
            "/api/v1/shoppinglists", data=dict(name="groceries"))
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], 'Authorization header must be set for a successful request')

    def test_post_shopping_list_fails_if_authorization_header_is_present_but_poorly_formatted(self):
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

        # Try adding a shopping list with a poorly formatted Authorization Header
        resp = self.test_client.post("/api/v1/shoppinglists",  # right word should be 'Bearer'*
                                     headers=dict(Authorization=f"Bearers {data['token']}"))
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "Authentication Header is poorly formatted. "
                             "The acceptable format is `Bearer <jwt_token>`")

    def test_post_shopping_list_fails_if_the_auth_token_has_expired_or_is_corrupted(self):
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

        # try adding a shoppinglist with an invalid token
        resp = self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries",
                  "notify date": "2018-03-14"},
            headers={"Authorization": f"Bearer {invalid_token}"})
        self.assertEqual(resp.status_code, 401)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "the given token is invalid. please re-login")

    def test_post_shopping_list_fails_if_that_list_already_exists(self):
        # Registering a user
        resp = self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "user with email 'testor@example.com' has been registered")
        self.assertEqual(data["status"], "success")

        # Logging in the registered user
        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "Login successful for 'testor@example.com'")
        self.assertEqual(data["status"], "success")
        self.assertIsNotNone(data["token"])

        token = data['token']

        # add 'groceries' to the user's shoppinglists
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers={'Authorization': f"Bearer {data['token']}"})
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], "'groceries' successfully created")

        #  Try to add groceries once more. IT SHOULD FAIL!
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers={'Authorization': f"Bearer {token}"})
        self.assertEqual(resp.status_code, 409)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'], "a shopping list with name 'groceries' already exists")

    def test_post_shopping_list_fails_if_name_is_not_given(self):
        # Registering a user
        resp = self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "user with email 'testor@example.com' has been registered")
        self.assertEqual(data["status"], "success")

        # Logging in the registered user
        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "Login successful for 'testor@example.com'")
        self.assertEqual(data["status"], "success")
        self.assertIsNotNone(data["token"])

        # Don't provide the name key in the data dictionary
        resp = self.test_client.post(
            "/api/v1/shoppinglists", headers={'Authorization': f"Bearer {data['token']}"})
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'], "'name' and 'notify date' of the shoppinglist are required fields")

    def test_get_shopping_list_is_successful_is_user_already_has_shoppinglists(self):
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

        # Add the first shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # Add the second shopping list to the logged in user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "furniture",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'furniture' successfully created")
        self.assertEqual(data["status"], "success")

        # Getting the user's shopping lists
        resp = self.test_client.get(
            "/api/v1/shoppinglists", headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], "success")
        self.assertIsInstance(data['lists'], list)

        # check the contents of data['lists']
        self.assertEqual(data['lists'][0]['name'], 'groceries')
        self.assertEqual(data['lists'][0]['id'], 1)
        self.assertEqual(data['lists'][1]['name'], 'furniture')
        self.assertEqual(data['lists'][1]['id'], 2)

    def test_get_shoppinglists_is_successful_if_the_user_has_not_added_a_shoppinglist(self):
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

        # Getting the user's shopping lists
        resp = self.test_client.get(
            "/api/v1/shoppinglists", headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], "success")
        self.assertEqual(data['message'], "No shoppinglists found!")

    def test_get_a_shopping_list_by_query_works_if_query_is_supplied(self):
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

        # Add the first shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # Add the second shopping list to the logged in user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "furniture",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'furniture' successfully created")
        self.assertEqual(data["status"], "success")

        # Getting the user's shopping lists by query
        resp = self.test_client.get(
            "/api/v1/shoppinglists?q=gr",
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], "success")
        self.assertIsInstance(data['matched lists'], list)
        self.assertEqual(len(data['matched lists']), 1)

        # check the contents of data['matched lists']
        self.assertEqual(data['matched lists'][0]['name'], 'groceries')
        self.assertEqual(data['matched lists'][0]['id'], 1)

    def test_get_shopping_list_by_query_works_if_query_matched_no_lists(self):
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

        # Add the first shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # Add the second shopping list to the logged in user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "furniture",
                                           "notify date": "2018-05-10"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'furniture' successfully created")
        self.assertEqual(data["status"], "success")

        # Getting the user's shopping lists using a non-existent query
        resp = self.test_client.get(
            "/api/v1/shoppinglists?q=xx", headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], "success")
        self.assertEqual(
            data['message'], "your query did not match any shopping lists")

    def test_get_shopping_list_fails_if_authorization_header_is_not_specified(self):
        resp = self.test_client.get("/api/v1/shoppinglists")
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], 'Authorization header must be set for a successful request')

    def test_get_shopping_lists_fails_if_authorization_header_is_present_but_poorly_formatted(self):
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

        # Get shoppinglists with a poorly formatted Authorization Header
        resp = self.test_client.get("/api/v1/shoppinglists",  # right word should be 'Bearer'*
                                    headers=dict(Authorization=f"Bearers {data['token']}"))
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "Authentication Header is poorly formatted. "
                             "The acceptable format is `Bearer <jwt_token>`")

    def test_get_shopping_lists_with_an_invalid_or_corrupted_token(self):
        invalid_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ" \
                        "9.eyJpYXQiOjE1MDg2MTExNjgs" + \
                        "ImV4cCI6MTUwODYxNDc2OCwic3ViIjoyfQ.I_W" \
                        "BI93N3PRlAXOasnXJ5QY4Zg0ggvNXA4b2B2CQ9g0"

        # getting shoppinglists with an invalid token
        resp = self.test_client.get(
            "/api/v1/shoppinglists", headers={"Authorization": f"Bearer {invalid_token}"})
        self.assertEqual(resp.status_code, 401)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "the given token is invalid. please re-login")

    def test_get_shoppinglists_paginates_output(self):
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

        # Add the first shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # Add the second shopping list to the logged in user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "furniture",
                                           "notify date": "2018-05-24"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'furniture' successfully created")
        self.assertEqual(data["status"], "success")

        # Add the third shoppinglist to the user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "cars",
                                           "notify date": "2018-07-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'cars' successfully created")
        self.assertEqual(data["status"], "success")

        # Getting the user's shopping lists for page 1
        resp = self.test_client.get(
            "/api/v1/shoppinglists?limit=1&page=1",
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'success')
        self.assertIsInstance(data['lists'], list)
        self.assertEqual(len(data['lists']), 1)

        self.assertEqual(data['lists'][0]['name'], 'groceries')
        self.assertEqual(data['lists'][0]['id'], 1)
        self.assertIsNone(data['previous page'])
        self.assertEqual(data['next page'],
                         '/api/v1/shoppinglists?page=2&limit=1')

        # Getting the user's shopping lists for page 2
        resp = self.test_client.get(
            "/api/v1/shoppinglists?limit=1&page=2",
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'success')
        self.assertIsInstance(data['lists'], list)
        self.assertEqual(len(data['lists']), 1)

        self.assertEqual(data['lists'][0]['name'], 'furniture')
        self.assertEqual(data['lists'][0]['id'], 2)
        self.assertEqual(data['previous page'],
                         '/api/v1/shoppinglists?page=1&limit=1')
        self.assertEqual(data['next page'],
                         '/api/v1/shoppinglists?page=3&limit=1')

    def test_get_shoppinglist_paginates_output_for_queried_URLs(self):
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

        # Add the first shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # Add the second shopping list to the logged in user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "furniture",
                                           "notify date": "2019-08-18"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'furniture' successfully created")
        self.assertEqual(data["status"], "success")

        # Add the third shoppinglist to the user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "books",
                                           "notify date": "2019-08-18"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'books' successfully created")
        self.assertEqual(data["status"], "success")

        # Getting the user's shopping lists for page 1
        resp = self.test_client.get(
            "/api/v1/shoppinglists?q=r&limit=1",
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'success')

        self.assertIsInstance(data['matched lists'], list)
        self.assertEqual(len(data['matched lists']), 1)

        self.assertEqual(data['matched lists'][0]['name'], 'groceries')
        self.assertEqual(data['matched lists'][0]['id'], 1)
        self.assertIsNone(data['previous page'])
        self.assertEqual(data['next page'],
                         '/api/v1/shoppinglists?page=2&limit=1&q=r')

        # Getting the user's shopping lists for page 2
        resp = self.test_client.get(
            "/api/v1/shoppinglists?q=r&limit=1&page=2",
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'success')
        self.assertIsInstance(data['matched lists'], list)
        self.assertEqual(len(data['matched lists']), 1)

        self.assertEqual(data['matched lists'][0]['name'], 'furniture')
        self.assertEqual(data['matched lists'][0]['id'], 2)
        self.assertIsNone(data['next page'])
        self.assertEqual(data['previous page'],
                         '/api/v1/shoppinglists?page=1&limit=1&q=r')


class TestShoppingListByID(BaseTests):
    def setUp(self):
        super(TestShoppingListByID, self).setUp()

    def test_get_shopping_list_by_id_is_successful(self):
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

        # Add the first shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # Add the second shopping list to the logged in user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "furniture",
                                           "notify date": "2017-12-23"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'furniture' successfully created")
        self.assertEqual(data["status"], "success")

        # Add the third shoppinglist to the user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "books",
                                           "notify date": "2017-12-23"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'books' successfully created")
        self.assertEqual(data["status"], "success")

        # Get first shoppinglist by id
        resp = self.test_client.get(
            "/api/v1/shoppinglists/1", headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data["id"], 1)
        self.assertEqual(data['name'], 'groceries')

        # get the second shoppinglist by id
        resp = self.test_client.get(
            "/api/v1/shoppinglists/2", headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data["id"], 2)
        self.assertEqual(data['name'], 'furniture')

    def test_get_shoppinglist_by_id_fails_if_list_id_is_not_an_integer(self):
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

        # Add the first shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # try to get a shoppinglist by using a string list_id
        resp = self.test_client.get(
            "/api/v1/shoppinglists/test", headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], 'failure')
        self.assertEqual(data['message'], "shopping list IDs must be integers")

    def test_get_shoppinglist_by_id_fails_if_list_id_is_an_integer_but_non_existent(self):
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

        # Add the first shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists", data={"name": "groceries", "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # try to get a shoppinglist with a non-existent ID
        resp = self.test_client.get(
            "/api/v1/shoppinglists/200", headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data)
        self.assertEqual(
            data['message'], "shopping list with that ID cannot be found!")
        self.assertEqual(data['status'], 'failure')

    def test_get_shopping_list_by_id_fails_for_no_authorization_header(self):
        resp = self.test_client.get("/api/v1/shoppinglists/2")
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], 'Authorization header must be set for a successful request')

    def test_delete_shopping_list_by_id_fails_for_no_authorization_header(self):
        resp = self.test_client.delete("/api/v1/shoppinglists/2")
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], 'Authorization header must be set for a successful request')

    def test_delete_shoppinglist_by_id_fails_if_list_id_is_an_integer_but_non_existent(self):
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

        # Add the first shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists", data={"name": "groceries", "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # try to delete a shoppinglist with a non-existent ID
        resp = self.test_client.delete(
            "/api/v1/shoppinglists/200", headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data)
        self.assertEqual(
            data['message'], "shopping list with that ID cannot be found!")
        self.assertEqual(data['status'], 'failure')

    def test_delete_shoppinglist_by_id_fails_if_list_id_is_not_an_integer(self):
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

        # Add the first shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists", data={"name": "groceries", "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # try to delete a shoppinglist by using a string list_id
        resp = self.test_client.delete(
            "/api/v1/shoppinglists/test", headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], 'failure')
        self.assertEqual(data['message'], "shopping list IDs must be integers")

    def test_delete_list_is_successful(self):
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

        # Add the first shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # Add the second shopping list to the logged in user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "furniture",
                                           "notify date": "2018-02-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'furniture' successfully created")
        self.assertEqual(data["status"], "success")

        # Get the lists to help in confirming whether the delete operation was successful
        resp = self.test_client.get(
            "/api/v1/shoppinglists", headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(len(data['lists']), 2)

        # Delete list with ID 1
        resp = self.test_client.delete(
            "/api/v1/shoppinglists/1", headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(
            data['message'], "shopping list with ID 1 deleted successfully")
        self.assertEqual(data['status'], 'success')

        # make a get request again to confirm the deletion
        resp = self.test_client.get(
            "/api/v1/shoppinglists", headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(len(data['lists']), 1)

    def test_put_is_successful_if_new_name_is_not_an_existing_list_name(self):
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

        # Add the first shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # Edit the list name to furniture
        resp = self.test_client.put("/api/v1/shoppinglists/1",
                                    data={"name": "furniture",
                                          "notify date": "2018-07-07"},
                                    headers=dict(
                                        Authorization=f'Bearer {token}')
                                    )
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "shoppinglist has been successfully edited!")
        self.assertEqual(data['data']['id'], 1)
        self.assertEqual(data['data']['name'], 'furniture')
        self.assertEqual(data['status'], 'success')

    def test_put_fails_if_notify_date_is_invalid(self):
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

        # Add the first shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # Edit the list name to furniture
        resp = self.test_client.put("/api/v1/shoppinglists/1",
                                    data={"name": "furniture",
                                          "notify date": "20yy-07-07"},
                                    headers=dict(
                                        Authorization=f'Bearer {token}')
                                    )
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data['message'], "dates must be specified as strings but with integer values")

    def test_put_fails_if_list_id_is_not_an_integer(self):
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

        # Add the first shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # try to edit a shoppinglist by using a string list_id
        resp = self.test_client.put(
            "/api/v1/shoppinglists/test",
            data=dict(name='furniture'),
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], 'failure')
        self.assertEqual(data['message'], "shopping list IDs must be integers")

    def test_put_fails_if_list_id_is_an_integer_but_non_existent_in_db(self):
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

        # Add the first shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # try to edit a shoppinglist with a non-existent ID
        resp = self.test_client.put(
            "/api/v1/shoppinglists/200",
            headers=dict(Authorization=f'Bearer {token}'),
            data=dict(name='books'))
        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data)
        self.assertEqual(
            data['message'], "shopping list with that ID cannot be found!")
        self.assertEqual(data['status'], 'failure')

    def test_put_fails_if_no_authorization_header_is_set(self):
        resp = self.test_client.put("/api/v1/shoppinglists/2")
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], 'Authorization header must be set for a successful request')

    def test_put_fails_if_new_name_is_similar_to_old_name(self):
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

        # Add the first shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # Try editing the list name to groceries
        resp = self.test_client.put("/api/v1/shoppinglists/1",
                                    data={"name": "groceries",
                                          "notify date": "2018-03-14"},
                                    headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data["message"], "No changes were made to the list")

    def test_put_fails_if_the_name_parameter_is_not_given(self):
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

        # Add the first shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        resp = self.test_client.put(
            "/api/v1/shoppinglists/1", headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'], "'name' and 'notify date' of the shoppinglist are required fields")

    def test_put_fails_if_new_name_already_exists(self):
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

        # Add the first shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "groceries",
                                           "notify date": "2018-03-14"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # Add the second shoppinglist
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "books",
                                           "notify date": "2033-12-04"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'books' successfully created")
        self.assertEqual(data["status"], "success")

        # Add the 3rd shoppinglist to the user
        resp = self.test_client.post("/api/v1/shoppinglists",
                                     data={"name": "furniture",
                                           "notify date": "2033-12-04"},
                                     headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'furniture' successfully created")
        self.assertEqual(data["status"], "success")

        # Edit the list name to furniture
        resp = self.test_client.put("/api/v1/shoppinglists/3",
                                    data={"name": "groceries",
                                          "notify date": "2018-03-14"},
                                    headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 409)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'], "a shopping list with name 'groceries' already exists")
