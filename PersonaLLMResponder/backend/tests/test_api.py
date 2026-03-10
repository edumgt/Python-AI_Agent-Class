from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from backend.app.main import app


class PersonaApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health(self) -> None:
        resp = self.client.get('/health')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get('status'), 'ok')


if __name__ == '__main__':
    unittest.main()
