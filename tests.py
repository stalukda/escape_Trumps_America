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

    # Getting error suggesting that I'm not getting to the right route or page
    def test_register(self):
        result = self.client.post('/register',
                                  data={'fname': "Sumaiya", 'lname': 'Talukdar',
                                  'email': "talukdar.sumaiya@gmail.com", 'password': 'Secret',
                                  'age': '10', 'zipcode': '94610', 'home_country': 'Bangladesh'},
                                  follow_redirects=True)
        self.assertIn("added.", result.data)

if __name__ == "__main__":
    unittest.main()
