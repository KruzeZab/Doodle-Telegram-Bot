from .meta import (
    YOUTUBE, 
    WIKIPEDIA, 
    LYRICS, 
    MOVIE, 
    URL, 
    WEATHER, 
    POLL,
    DICTIONARY
)

def handle_youtube(update, context):
    '''handle unexpected response'''
    update.message.reply_text("You must enter a valid video url.")
    return YOUTUBE

def handle_wikipedia(update, context):
    '''handle unexpected response'''
    update.message.reply_text("You must provide a valid title.")
    return WIKIPEDIA

def handle_song_lyrics(update, context):
    '''handle unexpected response'''
    update.message.reply_text("You must providea valid song title.")
    return LYRICS

def handle_url_shortener(update, context):
    '''handle unexpected response'''
    update.message.reply_text("You must provide a valid url.")
    return LYRICS

def handle_imdb_movie_review(update, context):
    '''handle unexpected response'''
    update.message.reply_text("You must provide a valid movie title.")
    return MOVIE

def handle_weather_info(update, context):
    '''handle unexpected response'''
    update.message.reply_text("You must provide a valid location.")
    return WEATHER

def handle_bad_poll(update, context):
    '''handle unexpected response'''
    update.message.reply_text("Press the button to create a poll.")
    return POLL

def handle_dictionary(update, context):
    '''handle unexpected response'''
    update.message.reply_text("Please enter a word.")
    return DICTIONARY
