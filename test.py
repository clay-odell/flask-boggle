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

    def test_word_submit(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [['Z', 'T', 'N', 'V', 'F'], ['I', 'C', 'Y', 'K', 'Q'], ['N', 'L', 'X', 'X', 'B'],['Y', 'S', 'T', 'A', 'R'], ['K', 'T', 'J', 'B', 'D']]
                
            response = client.get('/word-submit', query_string={'word': 'test'})
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('result', data)

    def test_post_score(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['highscore'] = 10
                sess['attempts'] = 5

        response = client.post('/post-score', json={'score': 15})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('newRecord', data)
        self.assertTrue(data['newRecord'])

        with client.session_transaction() as sess:
            self.assertEqual(sess['highscore'], 15)
            self.assertEqual(sess['attempts'], 6)

        response = client.post('/post-score', json={'score': 10})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('newRecord', data)
        self.assertFalse(data['newRecord'])

        with client.session_transaction() as sess:
            self.assertEqual(sess['highscore'], 15)
            self.assertEqual(sess['attempts'], 7)

if __name__ == '__main__':
    unittest.main()
