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
            self.assertEqual(session['high-score'], 0)
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
        """Tests if accessing the setup_game route returns a response with a 302 (redirect) status code and if the session is set up.
        Then, tests if accessing the setup_game route and following the redirect returns 'board.html'"""
        with app.test_client() as client:
            response = client.get('/setup-game')
            self.assertEqual(session['game-count'], 0)
            self.assertEqual(session['high-score'], 0)
            self.assertEqual(response.status_code, 302)
            response = client.get('/setup-game', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<title>A Game of Boggle</title>', response.get_data(as_text=True))

    def test_setup_game_session(self):
        """Tests if session values set from previous playthroughs are retained after accessing the setup_game route."""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['game-count'] = 5
                change_session['high-score'] = 10
            response = client.get('/setup-game')
            self.assertEqual(session['game-count'], 5)
            self.assertEqual(session['high-score'], 10)
    
    def test_show_board_redirect(self):
        """Tests if the show_board route will redirect to /setup-game if retrieving session['board'] fails."""
        with app.test_client() as client:
            response = client.get('/show-board')
            self.assertEqual(response.status_code, 302)
            response = client.get('show-board', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<title>A Game of Boggle</title>', response.get_data(as_text=True))

    def test_guess_redirect(self):
        """Tests if the guess route will redirect to /setup-game if retrieving session['board'] fails. Also tests if
        the guess route will redirect to /show-board if there are no query parameters."""
        with app.test_client() as client:
            response = client.get('/guess?guess=dog')
            self.assertEqual(response.status_code, 302)
            response=client.get('/guess?guess=dog', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(session['board'])
            self.assertIn('<title>A Game of Boggle</title>', response.get_data(as_text=True))
            with client.session_transaction() as change_session:
                boggle_game = Boggle()
                board = boggle_game.make_board()
                change_session['board'] = board
            response=client.get('/guess')
            self.assertEqual(response.status_code, 302)
            response=client.get('/guess', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<title>A Game of Boggle</title>', response.get_data(as_text=True))


    def test_guess_responses(self):
        """Tests if the guess route, when hit after all other relevant routes, 
        returns valid JSON of the {result: type_of_result} format that is expected. Also tests if
        session variables are initialized."""
        #It is possible to test easily for "not-word", and if something is a word the result will either be "not-on-board"
        #or "ok". However, I am uncertain if it is possible to test for "not-on-board" and "ok" seperately. In the interest of
        #time, I do not do so here.
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                boggle_game = Boggle()
                board = boggle_game.make_board()
                change_session['board'] = board
            response = client.get('/guess?guess=dog')
            self.assertEqual(session['game-count'], 0)
            self.assertEqual(session['high-score'], 0)
            possible_responses = ['{"result":"not-on-board"}', '{"result":"ok"}']
            self.assertIn(response.get_data(as_text=True).strip(), possible_responses)
            response = client.get('/guess?guess=adj')
            self.assertEqual(response.get_data(as_text=True).strip(), '{"result":"not-word"}')
            with client.session_transaction() as change_session:
                change_session['game-count'] = 10
                change_session['high-score'] = 30
            response = client.get('/guess?guess=adj')
            self.assertEqual(session['game-count'], 10)
            self.assertEqual(session['high-score'], 30)