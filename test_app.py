from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            #DONT FORGET STATUS CODE!!!!!!!!!
            #Thought: line break after labeling html and response
            self.assertEqual(response.status_code, 200)
            self.assertIn('<table class="board">', html)
            #...
            # test that you're getting a template

            # Careful of spacing 

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post('/api/new-game')
            response_data = response.get_json()
            response_game_id= response_data["game_id"]
            response_game_board= response_data["board"]

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response_game_id), str)
            self.assertTrue(type(response_game_board), list)
            self.assertIn(response_game_id, games)
    