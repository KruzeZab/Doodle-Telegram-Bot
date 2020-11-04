'''test meta files for tokens, etc...'''
import unittest
from enchantee import *


class TestMeta(unittest.TestCase):
    '''test for tokens and strings'''
    def test_BOT_TOKEN(self):
        '''test if bot token is valid'''
        self.assertIsInstance(BOT_TOKEN, str)
        self.assertIsNotNone(BOT_TOKEN, None)

    def test_LYRICS_TOKEN(self):
        '''test if bot token is valid'''
        self.assertIsInstance(BOT_TOKEN, str)
        self.assertIsNotNone(BOT_TOKEN, None)

    def test_MOVIE_TOKEN(self):
        '''test if movie token is valid'''
        self.assertIsInstance(MOVIE_TOKEN, str)
        self.assertIsNotNone(MOVIE_TOKEN, None)

    def test_WEATHER_TOKEN(self):
        '''test if weather token is valid'''
        self.assertIsInstance(WEATHER_TOKEN, str)
        self.assertIsNotNone(WEATHER_TOKEN, None)

    def test_help_text(self):
        '''test if help text is a string'''
        self.assertIsInstance(help_text, str)
    
    def test_MIN_CHOICE(self):
        '''test minimum choice'''
        self.assertEqual(MIN_CHOICE, 1)
        self.assertLessEqual(MIN_CHOICE, MAX_CHOICE)
    
    def test_MAX_CHOICE(self):
        '''test maximum choice'''
        self.assertGreaterEqual(MAX_CHOICE, MIN_CHOICE)

    def test_states(self):
        '''test conversation states
        for conversation handler'''
        self.assertIsNotNone(YOUTUBE)
        self.assertIsNotNone(WIKIPEDIA)
        self.assertIsNotNone(LYRICS)
        self.assertIsNotNone(MOVIE)
        self.assertIsNotNone(URL)
        self.assertIsNotNone(WEATHER)
        self.assertIsNotNone(DICTIONARY)
        self.assertIsNotNone(POLL)

if __name__ == '__main__':
    unittest.main()
