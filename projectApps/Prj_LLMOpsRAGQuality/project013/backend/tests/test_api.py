from __future__ import annotations

import unittest

try:
    from fastapi.testclient import TestClient
    from backend.app.main import app
except Exception:
    TestClient = None
    app = None


class ApiSmokeTests(unittest.TestCase):
    @unittest.skipIf(TestClient is None, "fastapi/testclient not installed")
    def test_health_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/health")
        self.assertEqual(resp.status_code, 200)
        payload = resp.json()
        self.assertEqual(payload.get("status"), "ok")


if __name__ == "__main__":
    unittest.main()
