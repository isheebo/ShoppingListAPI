import json
from datetime import datetime
import time
from tests import BaseTests


class TestShoppingListAPI(BaseTests):
    def test_post_shopping_list_is_successful(self):
        """ Given a name and a notify date, a shoppinglist can be created
        successfully. """
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        token = data["token"]

        resp = self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-2-13"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

    def test_post_shoppinglist_fails_for_invalid_format_notify_date(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        resp = self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "201x-03-14"},
            headers=dict(Authorization=f'Bearer {data["token"]}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data['message'],
            "dates must be specified as strings but with integer values")

    def test_post_fails_for_a_notify_date_with_year_before_today(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        token = data["token"]

        request_data = {"name": "groceries", "notify date": "1000-03-14"}

        resp = self.test_client.post(
            "/api/v1/shoppinglists",
            data=request_data,
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data['message'],
            "The year {} already passed, please use "
            "a valid year".format(request_data["notify date"].split("-")[0]))

    def test_post_fails_for_a_notify_date_with_year_beyond_2100(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        request_data = {"name": "groceries", "notify date": "2110-03-14"}
        resp = self.test_client.post(
            "/api/v1/shoppinglists",
            data=request_data,
            headers=dict(Authorization=f'Bearer {data["token"]}'))

        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data['message'],
            "By {}, you may be in afterlife, please consider years in "
            "range ({}-2099)".format(
                request_data["notify date"].split("-")[0],
                datetime.today().year))

    def test_post_shoppinglist_fails_for_month_that_has_already_passed(self):
        """ If the given 'notify date' is in this year, If the month
        specified in the date has already passed, post should fail:
        in this case, January 2018 has just passed. Feb 1st"""

        self.test_client.post(
            "/api/v1/auth/register",
            data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        request_data = {"name": "groceries", "notify date": "2018-01-01"}
        resp = self.test_client.post(
            "/api/v1/shoppinglists",
            data=request_data,
            headers=dict(Authorization=f'Bearer {data["token"]}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)

        # This was working in 2017. Doesn't work for 2018 January
        # updated on 1st Feb
        self.assertEqual(
            data['message'],
            "Invalid date, January 2018 has already passed by")

    def test_post_fails_for_date_that_has_already_passed(self):
        """ If the given 'notify date' is in this year, If the month
        specified in the date is the current month but the date specified
        has already passed, post should fail.
        """

        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        # This works when the year is 2018 Only!
        request_data = {"name": "groceries", "notify date": "2018-02-01"}

        resp = self.test_client.post(
            "/api/v1/shoppinglists",
            data=request_data,
            headers=dict(Authorization=f'Bearer {data["token"]}'))

        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data['message'],
            "Use dates starting from {}".format(
                datetime.now().strftime("%d/%m/%Y")))

    def test_post_shopping_list_fails_if_token_has_already_expired(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        time.sleep(4)  # enough time for the token to expire in testing mode.

        # try adding a shoppinglist.
        resp = self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {data["token"]}'))

        self.assertEqual(resp.status_code, 401)

        data = json.loads(resp.data)
        self.assertEqual(
            data['message'], "the token has expired: please re-login")

    def test_post_fails_if_no_authorization_header_is_specified(self):
        resp = self.test_client.post(
            "/api/v1/shoppinglists", data=dict(name="groceries"))
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"],
            'Authorization header must be set for a successful request')

    def test_post_fails_if_auth_header_is_present_but_poorly_formatted(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        # Try adding a list with a poorly formatted Authorization Header
        resp = self.test_client.post(
            "/api/v1/shoppinglists",
            headers=dict(Authorization=f"Bearers {data['token']}"))

        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "Authentication Header is poorly formatted. "
                             "The acceptable format is `Bearer <jwt_token>`")

    def test_post_fails_if_the_auth_token_has_expired_or_is_corrupted(self):
        invalid_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXjgs"

        resp = self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries",
                  "notify date": "2018-03-14"},
            headers={"Authorization": f"Bearer {invalid_token}"})

        self.assertEqual(resp.status_code, 401)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"],
            "the given token is invalid. please re-login")

    def test_post_shopping_list_fails_if_that_list_already_exists(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers={'Authorization': f"Bearer {data['token']}"})

        resp = self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers={'Authorization': f"Bearer {data['token']}"})

        self.assertEqual(resp.status_code, 409)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'],
            "a shopping list with name 'groceries' already exists")

    def test_post_shopping_list_fails_if_name_and_date_are_not_given(self):
        """ post should fail if no parameters are sent in the
        body of the request. """
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        # Don't provide the name key in the data dictionary
        resp = self.test_client.post(
            "/api/v1/shoppinglists",
            headers={'Authorization': f"Bearer {data['token']}"})

        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'],
            "'name' and 'notify date' of the shoppinglist "
            "are required fields")

    def test_get_succeeds_if_user_already_has_shoppinglists(self):
        """ If a user already has shoppinglists, they should
         returned as lists"""
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        token = data['token']

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "furniture", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.get(
            "/api/v1/shoppinglists",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], "success")
        self.assertIsInstance(data['lists'], list)

        # check the contents of data['lists']
        self.assertEqual(data['lists'][0]['name'], 'groceries')
        self.assertEqual(data['lists'][0]['id'], 1)
        self.assertEqual(data['lists'][1]['name'], 'furniture')
        self.assertEqual(data['lists'][1]['id'], 2)

    def test_get_succeeds_if_user_has_not_added_a_shoppinglist(self):
        """
        For user who has not added any lists yet, a message is returned
        and a status of success to indicate that the request
        was indeed successful
        """
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        token = data['token']

        # Getting the user's shopping lists
        resp = self.test_client.get(
            "/api/v1/shoppinglists",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], "success")
        self.assertEqual(data['message'], "No shoppinglists found!")

    def test_get_by_query_works_if_query_is_supplied(self):
        """Given a search query, all shoppinglists matching the query
        will be returned, that is, if there is any.
        """
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        token = data['token']

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "furniture", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

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

    def test_get_by_query_works_if_query_matched_no_lists(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        token = data['token']

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "furniture", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.get(
            "/api/v1/shoppinglists?q=xx",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], "success")
        self.assertEqual(
            data['message'],
            "your query did not match any shopping lists")

    def test_get_list_fails_if_authorization_header_is_not_specified(self):
        resp = self.test_client.get("/api/v1/shoppinglists")
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"],
            'Authorization header must be set for a successful request')

    def test_get_fails_if_auth_header_is_present_but_poorly_formatted(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        resp = self.test_client.get(
            "/api/v1/shoppinglists",
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

        resp = self.test_client.get(
            "/api/v1/shoppinglists",
            headers={"Authorization": f"Bearer {invalid_token}"})
        self.assertEqual(resp.status_code, 401)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "the given token is invalid. please re-login")

    def test_get_shoppinglists_paginates_output(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        token = data['token']

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "furniture", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "cars", "notify date": "2018-07-14"},
            headers=dict(Authorization=f'Bearer {token}'))

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

    def test_get_shoppinglist_paginates_output_for_queried_urls(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        token = data['token']

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "furniture", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "books", "notify date": "2018-07-14"},
            headers=dict(Authorization=f'Bearer {token}'))

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
