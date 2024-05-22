from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

import unittest

class FlaskTests(TestCase):
    def setUp(self):
        self.app = app
        self.client = app.test_client()
        
    def test_home(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [['Z', 'T', 'N', 'V', 'F'], ['I', 'C', 'Y', 'K', 'Q'], ['N', 'L', 'X', 'X', 'B'],['Y', 'S', 'T', 'A', 'R'], ['K', 'T', 'J', 'B', 'D']]
                sess['highscore'] = 0
                sess['attempts'] = 0

            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn('board', session)
            self.assertIn('highscore', session)
            self.assertIn('attempts', session)
            self.assertIsInstance(session['board'], list)
            self.assertIsInstance(session['highscore'], int)
            self.assertIsInstance(session['attempts'], int)

if __name__ == '__main__':
    unittest.main()
