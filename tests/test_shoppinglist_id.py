import json
from tests import BaseTests


class TestShoppingListByID(BaseTests):
    """ Tests for a single shoppinglist resource"""

    def test_get_shopping_list_by_id_is_successful(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        token = data['token']

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.get(
            "/api/v1/shoppinglists/1",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data["id"], 1)
        self.assertEqual(data['name'], 'groceries')

    def test_get_fails_if_list_id_is_not_an_integer(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        token = data['token']

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.get(
            "/api/v1/shoppinglists/test",
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], 'failure')
        self.assertEqual(data['message'],
                         "shopping list IDs must be integers")

    def test_get_fails_if_list_id_is_an_integer_but_non_existent(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        token = data['token']

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.get(
            "/api/v1/shoppinglists/200",
            headers=dict(Authorization=f'Bearer {token}'))

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
            data["message"],
            'Authorization header must be set for a successful request')

    def test_delete_list_by_id_fails_for_no_authorization_header(self):
        resp = self.test_client.delete("/api/v1/shoppinglists/2")
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"],
            'Authorization header must be set for a successful request')

    def test_delete_fails_if_list_id_is_an_integer_but_non_existent(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        token = data['token']

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        token = data['token']

        resp = self.test_client.delete(
            "/api/v1/shoppinglists/200",
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data)
        self.assertEqual(
            data['message'], "shopping list with that ID cannot be found!")
        self.assertEqual(data['status'], 'failure')

    def test_delete_fails_if_list_id_is_not_an_integer(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)

        data = json.loads(resp.data)
        token = data['token']

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.delete(
            "/api/v1/shoppinglists/test",
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], 'failure')
        self.assertEqual(data['message'],
                         "shopping list IDs must be integers")

    def test_delete_list_is_successful(self):
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
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "furniture", "notify date": "2018-02-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.get(
            "/api/v1/shoppinglists",
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(len(data['lists']), 2)

        # Delete list with ID 1
        resp = self.test_client.delete(
            "/api/v1/shoppinglists/1",
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(
            data['message'], "shopping list with ID 1 deleted successfully")
        self.assertEqual(data['status'], 'success')

        # make a get request again to confirm the deletion
        resp = self.test_client.get(
            "/api/v1/shoppinglists",
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(len(data['lists']), 1)

    def test_put_is_successful_if_new_name_is_not_an_existing_list_name(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        token = data['token']

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.put(
            "/api/v1/shoppinglists/1",
            data={"name": "furniture", "notify date": "2018-07-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "shoppinglist has been successfully edited!")
        self.assertEqual(data['data']['id'], 1)
        self.assertEqual(data['data']['name'], 'furniture')
        self.assertEqual(data['status'], 'success')

    def test_put_fails_if_notify_date_is_invalid(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        token = data['token']

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.put(
            "/api/v1/shoppinglists/1",
            data={"name": "furniture", "notify date": "20yy-07-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data['message'],
            "dates must be specified as strings but with integer values")

    def test_put_fails_if_list_id_is_not_an_integer(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        token = data['token']

        resp = self.test_client.put(
            "/api/v1/shoppinglists/test",
            data=dict(name='furniture'),
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], 'failure')
        self.assertEqual(data['message'], "shopping list IDs must be integers")

    def test_put_fails_if_list_id_is_an_integer_but_non_existent_in_db(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        token = data['token']

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
            data["message"],
            'Authorization header must be set for a successful request')

    def test_put_fails_if_no_changes_are_made_to_the_list(self):
        """ If the parameters provided in the request body are similar to
        the name and notify date of the list being edited, the request will
        fail since no changes are made with this kind of request.
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

        resp = self.test_client.put(
            "/api/v1/shoppinglists/1",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data["message"], "No changes were made to the list")

    def test_put_fails_if_the_name_and_notify_date_are_not_given(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        token = data['token']

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.put(
            "/api/v1/shoppinglists/1",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'],
            "'name' and 'notify date' of the shoppinglist "
            "are required fields")

    def test_put_fails_if_new_name_already_exists(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        token = data['token']

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-06-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "books", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.put(
            "/api/v1/shoppinglists/1",
            data={"name": "books", "notify date": "2018-02-22"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 409)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'],
            "a shopping list with name 'books' already exists")
