import json
from tests import BaseTests


class TestItemsAPIByID(BaseTests):
    def test_get_item_by_id_is_successful_for_a_given_list_and_item_id(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        # Login a User
        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        token = data["token"]

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-2-13"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists/1/items",
            data=dict(name="beans", price='3,500/=', quantity='1 kg'),
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists/1/items",
            data=dict(name="carrots", price='4,000/=', quantity='10'),
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists/1/items",
            data=dict(name="beans", price='3,500/=', quantity='1 kg'),
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists/1/items",
            data=dict(name="carrots", price='4,000/=', quantity='10'),
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.get(
            "/api/v1/shoppinglists/1/items/2",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['id'], 2)
        self.assertEqual(data['name'], 'carrots')

        # get the beans item
        resp = self.test_client.get(
            "/api/v1/shoppinglists/1/items/1",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['name'], 'beans')

    def test_get_fails_if_item_id_is_non_existent_on_the_shoppinglist(self):
        """ For an unknown integer ID, the get shoppinglist method
        should fail. """
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-2-13"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.get(
            "/api/v1/shoppinglists/1/items/2",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'], "item with that ID cannot be found!")

    def test_get_fails_if_shopping_list_with_list_id_is_non_existent(self):
        """ If an unknown list ID is used, getting an item should
         fail since the list is unknown"""
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        resp = self.test_client.get(
            "/api/v1/shoppinglists/100/items/1",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'], "shopping list with that ID cannot be found!")

    def test_get_item_by_id_fails_if_shopping_list_id_is_not_an_integer(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        resp = self.test_client.get(
            "/api/v1/shoppinglists/testing/items/1",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'], "shopping list IDs must be integers")

    def test_get_item_by_id_fails_if_item_id_is_not_an_integer(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-2-13"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.get(
            "/api/v1/shoppinglists/1/items/testing",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(data['message'], "item IDs must be integers")

    def test_get_item_by_id_fails_if_auth_header_is_not_specified(self):
        resp = self.test_client.get("/api/v1/shoppinglists/1/items/1")
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"],
            'Authorization header must be set for a successful request')

    def test_get_item_fails_if_auth_header_is_present_and_in_bad_format(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-2-13"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists/1/items",
            data=dict(name="beans", price='3,500/=', quantity='1 kg'),
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.get(
            "/api/v1/shoppinglists/1/items/1",
            headers=dict(Authorization=f'Bearers {token}'))
        self.assertEqual(resp.status_code, 403)

        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"],
            "Authentication Header is poorly formatted. "
            "The acceptable format is `Bearer <jwt_token>`")

    def test_delete_item_at_id_is_successful_given_a_list_and_item_id(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-2-13"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists/1/items",
            data=dict(name="beans", price='3,500/=', quantity='1 kg'),
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists/1/items",
            data=dict(name="carrots", price='4,000/=', quantity='10'),
            headers=dict(Authorization=f'Bearer {token}'))

        # delete the carrots item on the 'groceries' list
        resp = self.test_client.delete(
            "/api/v1/shoppinglists/1/items/2",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(
            data['message'],
            'an item with ID 2 has been successfully deleted')

    def test_delete_item_at_id_fails_if_item_id_is_not_an_integer(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)

        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-2-13"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-03-14"},
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.delete(
            "/api/v1/shoppinglists/1/items/testing",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(data['message'], "item IDs must be integers")

    def test_delete_item_at_id_fails_if_list_id_is_not_an_integer(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        resp = self.test_client.delete(
            "/api/v1/shoppinglists/testing/items/2",
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], 'failure')
        self.assertEqual(
            data['message'], "shopping list IDs must be integers")

    def test_delete_item_at_id_fails_if_id_is_non_existent_on_list(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-2-13"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists/1/items",
            data=dict(name="beans", price='3,500/=', quantity='1 kg'),
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.delete(
            "/api/v1/shoppinglists/1/items/200",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'], "item with that ID cannot be found!")

    def test_delete_item_at_id_fails_if_list_id_is_non_existent_in_db(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        resp = self.test_client.delete(
            "/api/v1/shoppinglists/100/items/1",
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'], "shopping list with that ID cannot be found!")

    def test_delete_item_at_id_fails_if_auth_header_is_not_specified(self):
        resp = self.test_client.delete("/api/v1/shoppinglists/1/items/1")
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"],
            'Authorization header must be set for a successful request')

    def test_delete_fails_if_auth_header_is_present_and_in_bad_format(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        resp = self.test_client.delete(
            "/api/v1/shoppinglists/1/items/1",
            headers=dict(Authorization=f'Bearers {token}'))
        self.assertEqual(resp.status_code, 403)

        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"],
            "Authentication Header is poorly formatted. "
            "The acceptable format is `Bearer <jwt_token>`")

    def test_put_item_at_id_is_successful(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-2-13"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists/1/items",
            data=dict(name="beans", price='3,500/=', quantity='1 kg'),
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.put(
            '/api/v1/shoppinglists/1/items/1',
            data=dict(name="fresh beans", price='3,500/=', quantity='1 kg'),
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['id'], 1)
        self.assertEqual(data['data']['name'], 'fresh beans')
        self.assertEqual(data['data']['price'], '3,500/=')
        self.assertEqual(
            data['message'], 'item has been updated successfully')

    def test_put_item_at_id_fails_if_item_is_None(self):
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-2-13"},
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.put(
            '/api/v1/shoppinglists/1/items/3',
            data=dict(name="fresh beans", price='3,500/=', quantity='1 kg'),
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'], "item with that ID cannot be found!")

    def test_put_fails_for_no_shoppinglist(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        resp = self.test_client.put(
            '/api/v1/shoppinglists/14/items/3',
            data=dict(name="fresh beans", price='3,500/=', quantity='1 kg'),
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'], "shopping list with that ID cannot be found!")

    def test_put_item_at_id_fails_if_no_changes_are_made_to_the_item(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-2-13"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists/1/items",
            data=dict(name="beans", price='3,500/=', quantity='1 kg'),
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.put(
            '/api/v1/shoppinglists/1/items/1',
            data=dict(name="beans", price='3,500/=', quantity='1 kg'),
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(data['message'],
                         "no changes were made to the item")

    def test_put_at_id_fails_if_another_item_with_the_new_name_exists(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-2-13"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists/1/items",
            data=dict(name="beans", price='3,500/=', quantity='1 kg'),
            headers=dict(Authorization=f'Bearer {token}')
        )

        self.test_client.post(
            "/api/v1/shoppinglists/1/items",
            data=dict(name="carrots", price='4,500/=', quantity='20'),
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.put(
            '/api/v1/shoppinglists/1/items/1',
            data=dict(name="carrots", price='3,500/=', quantity='17'),
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 409)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'], "an item with name 'carrots' already exists")

    def test_put_item_fails_if_all_form_fields_are_not_provided(self):
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login",
            data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post(
            "/api/v1/shoppinglists",
            data={"name": "groceries", "notify date": "2018-2-13"},
            headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists/1/items",
            data=dict(name="beans", price='3,500/=', quantity='1 kg'),
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.put(
            '/api/v1/shoppinglists/1/items/1',
            data=dict(name='fresh beans'),
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'],
            "'name', 'price' and 'quantity' of an item must "
            "be specified whereas 'status' is optional")

    def test_put_item_at_id_fails_if_auth_header_is_not_specified(self):
        resp = self.test_client.put(
            "/api/v1/shoppinglists/1/items/1",
            data=dict(name="beans", price='3,500/=', quantity='1 kg'))
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"],
            'Authorization header must be set for a successful request')

    def test_put_fails_if_auth_header_is_present_but_poorly_formatted(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        resp = self.test_client.put(
            "/api/v1/shoppinglists/1/items/1",
            data=dict(name="fresh beans", price='13,500/=', quantity='5 kg'),
            headers=dict(Authorization=f'Bearers {token}'))

        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"],
            "Authentication Header is poorly formatted. "
            "The acceptable format is `Bearer <jwt_token>`")
