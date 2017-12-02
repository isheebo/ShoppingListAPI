import json
from tests import BaseTests


class TestErrors(BaseTests):
    def setUp(self):
        super(TestErrors, self).setUp()

    def test_405_errors_are_handled_gracefully(self):
        resp = self.test_client.get("/api/v1/auth/login")
        self.assertEqual(resp.status_code, 405)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(
            data['message'], "method not allowed on this endpoint")

    def test_404_errors_are_handled_gracefully(self):
        resp = self.test_client.post("/api/v1/auth/login/")
        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'failure')
        self.assertEqual(data['message'], "resource not found on this URL")
