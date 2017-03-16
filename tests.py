import unittest
import server


class ServerTests(unittest.TestCase):
    """Tests for my server."""

    def setUp(self):
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    
    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("Escape Trump's America", result.data)


if __name__ == "__main__":
    unittest.main()