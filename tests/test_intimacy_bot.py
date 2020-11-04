'''test intimacy file for handlers, etc...'''
from telegram.ext import Updater, ConversationHandler
import unittest
from enchantee import *


class TestIntimacyBot(unittest.TestCase):
    '''test for action handlers of conversation'''
    def test_states(self):
        '''test conversation steps'''
        self.assertIsNotNone(NAME)
        self.assertIsNotNone(GENDER)
        self.assertIsNotNone(AGE)
        self.assertIsNotNone(PHOTO)
        self.assertIsNotNone(SKIP_PHOTO)
        self.assertIsNotNone(ADDRESS)
        self.assertIsNotNone(BIO)

    def test_intimacy_bot(self):
        '''test main 
        conversation handler method'''
        self.assertIsInstance(intimacy_quiz(), ConversationHandler)

if __name__ == '__main__':
    unittest.main()
    