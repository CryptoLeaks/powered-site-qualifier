import unittest

from starlette.requests import Request

from app.main import SiteQualificationRequest, app, health, landing_page, paid_qualify


class AppTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(app)

    def test_root_is_html_landing_page(self):
        response = landing_page()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.media_type, "text/html")
        self.assertIn("charset=utf-8", response.headers["content-type"])
        self.assertIn("Powered-Site Qualifier", response.body.decode())
        self.assertIn("Site Data", response.body.decode())

    def test_health_and_paid_boundary_remain_available(self):
        self.assertEqual(health()["status"], "ok")
        scope = {"type": "http", "method": "POST", "path": "/v1/paid/qualify", "headers": [], "query_string": b"", "scheme": "http", "server": ("testserver", 80), "client": ("testclient", 50000), "root_path": ""}
        response = paid_qualify(Request(scope), SiteQualificationRequest())
        self.assertEqual(response.status_code, 402)


if __name__ == "__main__":
    unittest.main()
