from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
import string


class FlaskTests(TestCase):
    def test_display_start(self):
        """Tests if accessing the root route sets session['game-count'] to 0 and session['high-score'] to None.
        Also tests if accessing the root route returns 'start_game.html'"""
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(session['game-count'], 0)
            self.assertIsNone(session['high-score'])
            self.assertIn('<title>Starting the Game</title>', response.get_data(as_text=True))

#https://www.geeksforgeeks.org/python-unittest-assertin-function/ First key, then container.
#https://docs.python.org/3/library/functions.html#isinstance More assert methods.
    def test_setup_game_board_attributes(self):
        """Tests if accessing the setup_game route creates a boggle board--a list of five lists with five characters from string.ascii.uppercase
         in each--and stores it in session['board']"""
        with app.test_client() as client:
            response = client.get('/setup-game')
            self.assertIsInstance(session['board'], list)
            self.assertEqual(len(session['board']), 5)
            for possibleList in session['board']:
                self.assertIsInstance(possibleList, list)
                self.assertEqual(len(possibleList), 5)
                for possibleCharacter in possibleList:
                    self.assertIn(possibleCharacter, string.ascii_uppercase)
                    self.assertEqual(len(possibleCharacter), 1)

    def test_setup_game_requests(self):
        """Tests if accessing the setup_game route returns a response with a 302 (redirect) status code.
        Then, tests if accessing the setup_game route and following the redirect returns 'board.html'"""
        with app.test_client() as client:
            response = client.get('/setup-game')
            self.assertEqual(response.status_code, 302)
            response = client.get('/setup-game', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<title>A Game of Boggle</title>', response.get_data(as_text=True))
