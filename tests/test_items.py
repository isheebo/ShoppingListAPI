import json
from tests import BaseTests


class TestItemsAPI(BaseTests):
    def test_post_item_is_successful_if_all_parameters_are_given(self):
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        # Login a User
        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        # Add a shoppinglist to a user
        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        # add item to the shoppinglist 'groceries'
        resp = self.test_client.post("/api/v1/shoppinglists/1/items",
                                     data=dict(name="beans", price='3,500/=',
                                               quantity='1 kg'),
                                     headers=dict(
                                         Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'beans' has been added")
        self.assertEqual(data['status'], 'success')

    def test_post_item_fails_if_item_with_that_name_already_exists(self):
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        # Add a shoppinglist to a user
        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        # add beans to the shoppinglist 'groceries'
        self.test_client.post("/api/v1/shoppinglists/1/items",
                              data=dict(name="beans", price='3,500/=',
                                        quantity='1 kg'),
                              headers=dict(Authorization=f'Bearer {token}'))

        # try re-adding 'beans' to the groceries shoppinglist
        resp = self.test_client.post("/api/v1/shoppinglists/1/items",
                                     data=dict(name="beans", price='3,500/=',
                                               quantity='1 kg'),
                                     headers=dict(
                                         Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 409)  # No conflicts allowed
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "an item with name 'beans' already exists")
        self.assertEqual(data['status'], 'failure')

    def test_post_item_fails_if_either_name_quantity_price_are_not_given(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        # Login a User
        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        # Add a shoppinglist to a user
        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        # try adding 'beans' to 'groceries' with out specifying its quantity
        resp = self.test_client.post("/api/v1/shoppinglists/1/items",
                                     data=dict(name="beans",
                                               price='3,500/='),
                                     headers=dict(
                                         Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"],
            "'name', 'price' and 'quantity' of an item "
            "must be specified whereas 'status' is optional")

        self.assertEqual(data['status'], 'failure')

    def test_post_item_fails_if_the_given_list_id_is_not_an_integer(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        # Login a User
        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        # use a URL with a string ID `testing`
        resp = self.test_client.post("/api/v1/shoppinglists/testing/items",
                                     data=dict(
                                         name="beans",
                                         price='3,500/=', quantity='1 kg'),
                                     headers=dict(
                                         Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], 'failure')
        self.assertEqual(data['message'], "shopping list IDs must be integers")

    def test_post_item_fails_if_list_id_is_an_integer_but_non_existent(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        # Login a User
        resp = self.test_client.post("/api/v1/auth/login",
                                     data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        # try adding to a non-existent ID
        resp = self.test_client.post("/api/v1/shoppinglists/100/items",
                                     data=dict(name="beans", price='3,500/=',
                                               quantity='1 kg'),
                                     headers=dict(
                                         Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'], "shopping list with that ID cannot be found!")

    def test_post_item_fails_if_authorization_header_is_not_specified(self):
        resp = self.test_client.post("/api/v1/shoppinglists/1/items",
                                     data=dict(
                                         name="beans",
                                         price='3,500/=', quantity='1 kg'))
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"],
            'Authorization header must be set for a successful request')

    def test_post_item_fails_if_authorization_header_is_specified_but_poorly_formatted(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        # Login a User
        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        # Add a shoppinglist to a user
        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        # add item to the shoppinglist 'groceries'
        resp = self.test_client.post("/api/v1/shoppinglists/1/items",
                                     data=dict(name="beans", price='3,500/=',
                                               quantity='1 kg'),
                                     headers=dict(
                                         Authorization=f'Bearers {token}'))
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"],
            "Authentication Header is poorly formatted. "
            "The acceptable format is `Bearer <jwt_token>`")

    def test_get_items_is_successful_if_there_are_items_that_have_been_added_to_the_list(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        # Login a User
        resp = self.test_client.post(
            "/api/v1/auth/login",
            data=self.user_data)

        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        # Add a shoppinglist to a user
        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        # add 'beans' to the shoppinglist 'groceries'
        self.test_client.post("/api/v1/shoppinglists/1/items",
                              data=dict(name="beans", price='3,500/=',
                                        quantity='1 kg'),
                              headers=dict(Authorization=f'Bearer {token}'))

        # add 'carrots' to the list
        self.test_client.post("/api/v1/shoppinglists/1/items",
                              data=dict(name="carrots", price='4,000/=',
                                        quantity='10'),
                              headers=dict(Authorization=f'Bearer {token}'))

        # get the items on the 'groceries' list
        resp = self.test_client.get(
            "/api/v1/shoppinglists/1/items",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'success')
        self.assertIsInstance(data['items'], list)
        self.assertEqual(len(data['items']), 2)

    def test_get_items_is_successful_if_no_items_have_been_added_to_the_list_yet(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        # Login a User
        resp = self.test_client.post(
            "/api/v1/auth/login",
            data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        # Add a shoppinglist to a user
        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        # get the items on the 'groceries' list
        resp = self.test_client.get(
            "/api/v1/shoppinglists/1/items",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'no items on this list')

    def test_get_items_passes_if_the_database_is_being_queried_and_there_are_items_on_that_list(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2020-09-29"},
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post("/api/v1/shoppinglists/1/items",
                              data=dict(name="beans", price='3,500/=',
                                        quantity='1 kg'),
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post("/api/v1/shoppinglists/1/items",
                              data=dict(name="carrots", price='4,000/=',
                                        quantity='10'),
                              headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.get(
            "/api/v1/shoppinglists/1/items?q=ca",
            headers=dict(Authorization=f'Bearer {token}'))  # for carrots

        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'success')
        self.assertIsInstance(data['matched items'], list)
        self.assertEqual(len(data['matched items']), 1)

    def test_get_items_passes_if_the_database_is_being_queried_and_no_items_on_list(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        # Login a User
        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        # Add a shoppinglist to a user
        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        # try getting items on the 'groceries' list by querying the list
        resp = self.test_client.get(
            "/api/v1/shoppinglists/1/items?q=ca",
            headers=dict(Authorization=f'Bearer {token}'))  # returns None

        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], "your query did not match any items")

    def test_get_items_fails_if_no_authorization_header_is_specified(self):
        resp = self.test_client.get("/api/v1/shoppinglists/1/items")
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], 'Authorization header must be set for a successful request')

    def test_get_items_fails_if_authorization_header_is_specified_but_poorly_formatted(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        # Login a User
        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        # Add a shoppinglist to a user
        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        # add 'beans' to the shoppinglist 'groceries'
        self.test_client.post("/api/v1/shoppinglists/1/items",
                              data=dict(name="beans", price='3,500/=',
                                        quantity='1 kg'),
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post("/api/v1/shoppinglists/1/items",
                              data=dict(name="carrots", price='4,000/=',
                                        quantity='10'),
                              headers=dict(Authorization=f'Bearer {token}'))

        # get the items on the 'groceries' list
        resp = self.test_client.get(
            "/api/v1/shoppinglists/1/items",
            headers=dict(Authorization=f'Bearers {token}'))

        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"],
            "Authentication Header is poorly formatted. "
            "The acceptable format is `Bearer <jwt_token>`")

    def test_get_items_fails_if_list_ID_is_an_integer_but_non_existent_in_the_database(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        # Login a User
        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        # try getting from a non-existent ID
        resp = self.test_client.get(
            "/api/v1/shoppinglists/100/items",
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'], "shopping list with that ID cannot be found!")

    def test_get_items_fails_if_list_id_is_not_an_integer(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        # Login a User
        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        # use a URL with a string ID `testing`
        resp = self.test_client.get(
            "/api/v1/shoppinglists/testing/items",
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], 'failure')
        self.assertEqual(data['message'], "shopping list IDs must be integers")


class TestItemsAPIByID(BaseTests):
    def test_get_item_by_id_is_successful_for_a_given_list_and_item_id(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        # Login a User
        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)

        token = data["token"]

        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post("/api/v1/shoppinglists/1/items",
                              data=dict(name="beans", price='3,500/=',
                                        quantity='1 kg'),
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post("/api/v1/shoppinglists/1/items",
                              data=dict(name="carrots", price='4,000/=',
                                        quantity='10'),
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post("/api/v1/shoppinglists/1/items",
                              data=dict(name="beans", price='3,500/=',
                                        quantity='1 kg'),
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post("/api/v1/shoppinglists/1/items",
                              data=dict(name="carrots", price='4,000/=',
                                        quantity='10'),
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

    def test_get_item_by_id_fails_if_item_id_is_non_existent_on_the_shoppinglist(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-03-14"},
                              headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.get(
            "/api/v1/shoppinglists/1/items/2",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(data['message'], "item with that ID cannot be found!")

    def test_get_item_by_id_fails_if_shopping_list_with_list_id_is_non_existent(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post(
            "/api/v1/auth/login",
            data=self.user_data)
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
            "/api/v1/auth/login",
            data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        resp = self.test_client.get(
            "/api/v1/shoppinglists/testing/items/1",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(data['message'], "shopping list IDs must be integers")

    def test_get_item_by_id_fails_if_item_id_is_not_an_integer(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-03-14"},
                              headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.get(
            "/api/v1/shoppinglists/1/items/testing",
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(data['message'], "item IDs must be integers")

    def test_get_item_by_id_fails_if_authorization_header_is_not_specified(self):
        resp = self.test_client.get("/api/v1/shoppinglists/1/items/1")
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"],
            'Authorization header must be set for a successful request')

    def test_get_item_by_id_fails_if_authorization_header_is_present_but_poorly_formatted(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-03-14"},
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post("/api/v1/shoppinglists/1/items",
                              data=dict(name="beans", price='3,500/=',
                                        quantity='1 kg'),
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

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post("/api/v1/shoppinglists",
                              data={
                                  "name": "groceries",
                                  "notify date": "2018-03-14"},
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post("/api/v1/shoppinglists/1/items",
                              data=dict(name="beans", price='3,500/=',
                                        quantity='1 kg'),
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post("/api/v1/shoppinglists/1/items",
                              data=dict(name="carrots", price='4,000/=',
                                        quantity='10'),
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
            "/api/v1/auth/login",
            data=self.user_data)

        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-03-14"},
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

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        resp = self.test_client.delete(
            "/api/v1/shoppinglists/testing/items/2",
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], 'failure')
        self.assertEqual(data['message'], "shopping list IDs must be integers")

    def test_delete_item_at_id_fails_if_item_id_is_an_integer_but_non_existent_in_list(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post("/api/v1/shoppinglists/1/items",
                              data=dict(name="beans", price='3,500/=',
                                        quantity='1 kg'),
                              headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.delete(
            "/api/v1/shoppinglists/1/items/200", headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(data['message'], "item with that ID cannot be found!")

    def test_delete_item_at_id_fails_if_list_id_is_non_existent_in_db(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
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

    def test_delete_item_at_id_fails_if_authorization_header_is_not_specified(self):
        resp = self.test_client.delete("/api/v1/shoppinglists/1/items/1")
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"],
            'Authorization header must be set for a successful request')

    def test_delete_item_at_id_fails_if_authorization_header_is_present_but_poorly_formatted(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
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

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post("/api/v1/shoppinglists/1/items",
                              data=dict(name="beans", price='3,500/=',
                                        quantity='1 kg'),
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
        self.assertEqual(data['message'], 'item has been updated successfully')

    def test_put_item_at_id_fails_if_item_is_None(self):
        self.test_client.post(
            "/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.put('/api/v1/shoppinglists/1/items/3',
                                    data=dict(name="fresh beans", price='3,500/=',
                                              quantity='1 kg'),
                                    headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(data['message'],
                         "item with that ID cannot be found!")

    def test_put_fails_for_no_shoppinglist(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        resp = self.test_client.put(
            '/api/v1/shoppinglists/14/items/3',
            data=dict(name="fresh beans", price='3,500/=',
                      quantity='1 kg'),
            headers=dict(Authorization=f'Bearer {token}'))

        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(data['message'],
                         "shopping list with that ID cannot be found!")

    def test_put_item_at_id_fails_if_no_changes_are_made_to_the_item(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists/1/items",
            data=dict(name="beans", price='3,500/=',
                      quantity='1 kg'),
            headers=dict(Authorization=f'Bearer {token}'))

        resp = self.test_client.put(
            '/api/v1/shoppinglists/1/items/1',
            data=dict(name="beans", price='3,500/=',
                      quantity='1 kg'),
            headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(data['message'],
                         "no changes were made to the item")

    def test_put_item_at_id_fails_if_another_item_with_the_new_name_exists(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        self.test_client.post("/api/v1/shoppinglists",
                              data={"name": "groceries",
                                    "notify date": "2018-2-13"},
                              headers=dict(Authorization=f'Bearer {token}'))

        self.test_client.post(
            "/api/v1/shoppinglists/1/items",
            data=dict(name="beans", price='3,500/=',
                      quantity='1 kg'),
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
        self.assertEqual(data['message'],
                         "an item with name 'carrots' already exists")

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

    def test_put_item_at_id_fails_if_authorization_header_is_not_specified(self):
        resp = self.test_client.put(
            "/api/v1/shoppinglists/1/items/1", data=dict(
                name="beans", price='3,500/=', quantity='1 kg'))
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"],
            'Authorization header must be set for a successful request')

    def test_put_item_at_id_fails_if_auth_header_is_present_but_poorly_formatted(self):
        self.test_client.post("/api/v1/auth/register", data=self.user_data)

        resp = self.test_client.post("/api/v1/auth/login", data=self.user_data)
        data = json.loads(resp.data)
        self.assertIsNotNone(data["token"])

        token = data["token"]

        resp = self.test_client.put(
            "/api/v1/shoppinglists/1/items/1",
            data=dict(name="fresh beans", price='13,500/=',
                      quantity='5 kg'),
            headers=dict(Authorization=f'Bearers {token}'))

        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"],
            "Authentication Header is poorly formatted. "
            "The acceptable format is `Bearer <jwt_token>`")
