import json
from tests import BaseTests


class TestItemsAPI(BaseTests):
    def setUp(self):
        super(TestItemsAPI, self).setUp()

    def test_post_item_is_successful_if_all_parameters_are_given(self):
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

        token = data["token"]

        # Add a shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists", data=dict(
            name="groceries"), headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # add item to the shoppinglist 'groceries'
        resp = self.test_client.post("/api/v1/shoppinglists/1/items", data=dict(
            name="beans", price='3,500/=', quantity='1 kg'), headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'beans' has been added")
        self.assertEqual(data['status'], 'success')

    def test_post_item_fails_if_item_with_that_name_already_exists(self):
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

        token = data["token"]

        # Add a shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists", data=dict(
            name="groceries"), headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # add beans to the shoppinglist 'groceries'
        resp = self.test_client.post("/api/v1/shoppinglists/1/items", data=dict(
            name="beans", price='3,500/=', quantity='1 kg'), headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'beans' has been added")
        self.assertEqual(data['status'], 'success')

        # try re-adding 'beans' to the groceries shoppinglist
        resp = self.test_client.post("/api/v1/shoppinglists/1/items", data=dict(
            name="beans", price='3,500/=', quantity='1 kg'), headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 409)  # No conflicts allowed
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "an item with name 'beans' already exists")
        self.assertEqual(data['status'], 'failure')

    def test_post_item_fails_if_either_name_quantity_price_are_not_given(self):
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

        token = data["token"]

        # Add a shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists", data=dict(
            name="groceries"), headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # try adding 'beans' to 'groceries' with out specifying its quantity
        resp = self.test_client.post("/api/v1/shoppinglists/1/items", data=dict(  # quantity not given
            name="beans", price='3,500/='), headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(
            data["message"], "'name', 'price' and 'quantity' of an item must be specified whereas 'status' is optional")
        self.assertEqual(data['status'], 'failure')

    def test_post_item_fails_if_the_given_list_id_is_not_an_integer(self):
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

        token = data["token"]

        # Add a shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists", data=dict(
            name="groceries"), headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # use a URL with a string ID `testing`
        resp = self.test_client.post("/api/v1/shoppinglists/testing/items", data=dict(
            name="beans", price='3,500/=', quantity='1 kg'), headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], 'failure')
        self.assertEqual(data['message'], "shopping list IDs must be integers")

    def test_post_item_fails_if_list_id_is_an_integer_but_non_existent(self):
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

        token = data["token"]

        # Add a shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists", data=dict(
            name="groceries"), headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # try adding to a non-existent ID
        resp = self.test_client.post("/api/v1/shoppinglists/100/items", data=dict(
            name="beans", price='3,500/=', quantity='1 kg'), headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'], "shopping list with that ID cannot be found!")

    def test_post_item_fails_if_authorization_header_is_not_specified(self):
        resp = self.test_client.post("/api/v1/shoppinglists/1/items", data=dict(
            name="beans", price='3,500/=', quantity='1 kg'))
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], 'Authorization header must be set for a successful request')

    def test_post_item_fails_if_authorization_header_is_specified_but_poorly_formatted(self):
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

        token = data["token"]

        # Add a shoppinglist to a user
        resp = self.test_client.post("/api/v1/shoppinglists", data=dict(
            name="groceries"), headers=dict(Authorization=f'Bearer {token}'))
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data["message"], "'groceries' successfully created")
        self.assertEqual(data["status"], "success")

        # add item to the shoppinglist 'groceries'
        resp = self.test_client.post("/api/v1/shoppinglists/1/items", data=dict(
            name="beans", price='3,500/=', quantity='1 kg'), headers=dict(Authorization=f'Bearers {token}'))
        self.assertEqual(resp.status_code, 403)
        data = json.loads(resp.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(
            data["message"], "Authentication Header is poorly formatted. The acceptable format is `Bearer <jwt_token>`")
