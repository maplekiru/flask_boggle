from unittest import TestCase

from app import app, games
from boggle import BoggleGame

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

            # check for ok response and correct html
            self.assertEqual(response.status_code, 200)
            self.assertIn('<table', html)
       

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.get('/api/new-game')
            # breakpoint()
            # {"gameId": "need-real-id", "board": "need-real-board"}
            new_game_data = response.get_json()
            print('new_game_data:', new_game_data)
            uniqueId = new_game_data['gameId']

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(games[uniqueId], BoggleGame)
            self.assertIsInstance(new_game_data['board'], list)


    def test_score_word(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.get('/api/new-game')
            # breakpoint()
            # {"gameId": "need-real-id", "board": "need-real-board"}
            new_game_data = response.get_json()
            print('new_game_data:', new_game_data)
            uniqueId = new_game_data['gameId']

            game = games[uniqueId]
            game.board = [["C","A","T"],["A","V","T"],["A","B","E"]]
            game.board_size = 3
            # print('result', game.board, games)

            resp = client.post('/api/score-word',
                json={'word': 'CAT', 'game_id': uniqueId})
            result = resp.get_json()
            print('result:', result['result'])
            self.assertEqual(result['result'],'ok')

            resp = client.post('/api/score-word',
                json={'word': 'ABC', 'game_id': uniqueId})
            result = resp.get_json()
            print('result:', result['result'])
            self.assertEqual(result['result'],'not-word')

            resp = client.post('/api/score-word',
                json={'word': 'TAB', 'game_id': uniqueId})
            result = resp.get_json()
            print('result:', result['result'])
            self.assertEqual(result['result'],'not-on-board')
            
