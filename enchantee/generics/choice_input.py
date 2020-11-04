'''
Ask for extra input data
'''
from telegram import KeyboardButton, KeyboardButtonPollType, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from generics.meta import (
    YOUTUBE,
    WIKIPEDIA,
    LYRICS,
    MOVIE,
    URL,
    WEATHER,
    DICTIONARY,
    POLL
)
from .typing_action import send_typing_action


@send_typing_action
def youtube_input(update, context): #requires action
    '''ask for youtube url'''
    update.message.reply_text("Please enter the url of the video:")
    return YOUTUBE

@send_typing_action
def wikipedia_input(update, context): #requires action
    '''ask the title of wiki'''
    update.message.reply_text("Please enter the wikipedia title:")
    return WIKIPEDIA

@send_typing_action
def song_lyrics_input(update, context): #requires action
    '''get song lyrics'''
    update.message.reply_text("Please enter the song title:")
    return LYRICS

@send_typing_action
def movie_review_input(update, context): #requires action
    '''ask for movie name'''
    update.message.reply_text("Please enter the movie title:")
    return MOVIE

@send_typing_action
def url_shortener_input(update, context): #requires action
    '''ask for url'''
    update.message.reply_text("Please enter the url:")
    return URL

@send_typing_action
def weather_input(update, context): # requires action
    '''ask for location'''
    context.bot_data['choice'] = update.message.text
    update.message.reply_text("Please enter the city name:")
    return WEATHER

@send_typing_action
def dictionary_input(update, context):
    '''ask for word to get meaning'''
    update.message.reply_text("Please enter the word:")
    return DICTIONARY

@send_typing_action
def poll_input(update, context):
    '''show button for poll creation'''
    button = [[KeyboardButton("Create a Poll", request_poll=KeyboardButtonPollType())]]
    message = "Press the button to create a poll."
    update.effective_message.reply_text(
        message, reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True)
    )
    return POLL
