'''
Handler for all the state actions
'''
from random import randint
import os, requests, wikipedia
from telegram import ReplyKeyboardRemove, ParseMode
from pytube import YouTube
from pyshorteners import Shortener
from lyricsgenius import Genius
from PyDictionary import PyDictionary
from telegram.ext import ConversationHandler
from .meta import (
    MIN_CHOICE, 
    MAX_CHOICE, 
    LYRICS_TOKEN, 
    MOVIE_TOKEN, 
    WEATHER_TOKEN,
    
    YOUTUBE,
)
from .typing_action import send_typing_action

def convert_to_celsius(kelvin):
    '''convert kelvin to celsius'''
    return kelvin - 273.15

def movie_to_str(update, context, data):
    '''
    helper func to formalte string from
    the given data and send to the user
    '''
    title = data.get('original_title', '')
    release_date = data.get('release_date', '')
    rating = data.get('vote_average', '')
    total_votes = data.get('vote_count', '')
    summary = data.get('overview', '')
    image_url = 'http://image.tmdb.org/t/p/w300_and_h450_bestv2'
    uri_image = data.get('poster_path', '')
    if uri_image:
        image_url += uri_image
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url)
    text = f'''\
    Title: <strong>{title}</strong>\nReleased Date: <strong>{release_date}</strong>\nVotings: <strong>{total_votes}</strong>\nRating: <strong>{rating}</strong>\nSummary: {summary}\
    '''
    update.message.reply_text(text, parse_mode=ParseMode.HTML)

@send_typing_action
def youtube_downloader(update, context):
    '''convert youtube to mp3'''
    url = update.message.text
    try:
        number = randint(1, 100000)
        yt = YouTube(url)
        update.message.reply_text("Processing video. We will notify you as soon as the video is ready for download.")
        stream = yt.streams.first()
        stream.download(filename=f'download-{number}')
        context.bot.send_video(chat_id=update.effective_chat.id, video=open(f'./download-{number}.mp4', 'rb'), supports_streaming=True, timeout=60*60)
        update.message.reply_text("Your video is ready for download.")
        os.remove(f'./download-{number}.mp4')
        update.message.reply_text("Use /help to list available actions.")
    except:
        update.message.reply_text("Invalid url or permission denied to download the video. Please try again.")
    return ConversationHandler.END

@send_typing_action
def wikipedia_summary(update, context):
    '''return wikipedia summary'''
    result = ""
    text = update.message.text
    try:
        result = wikipedia.summary(text)
        update.message.reply_text(result)
    except:
        update.message.reply_text("Summary not found for " + text + ".")
    update.message.reply_text("Use /help to list available actions.")
    return ConversationHandler.END

@send_typing_action
def send_random_joke(update, context):
    '''send a random joke'''
    jokes = [
        "How do you tell if a vampire is sick? - By how much he is coffin lol 😂",
        "Why did the bike fall over?- It was two tired. 😂",
        "I'm a big fan of whiteboards. I find them quite re-markable. 😂",
        "What do you call an animal you keep in your car? - Carpet 😂",
        "Why did the crab never share? - Because he's shellfish 😂",
        "Two guys stole a calendar. They got six months each. 😂",
        "What do you call a guy who’s had too much to drink? - A cab. 😂",
        "What was the dogs favorite type of homework to do? - A lab report 😂",
        "What’s the best thing about Switzerland? - I don’t know, but the flag is a big plus. 😂",
        "I invented a new word: - Plagiarism! 😂",
        "Did you hear about the actor who fell through the floorboards? - He was just going through a stage. 😂",
        "Did you hear about the claustrophobic astronaut? - He just needed a little space. 😂"
    ]
    selected = randint(0, len(jokes)-1)
    update.message.reply_text(f"<strong>{jokes[selected]}</strong>", parse_mode=ParseMode.HTML)
    update.message.reply_text("Use /help to list available actions.")
    return ConversationHandler.END

@send_typing_action
def retrieve_song_lyrics(update, context):
    '''get song lyrics'''
    text = update.message.text
    genius = Genius(LYRICS_TOKEN)
    genius.skip_non_songs = True
    song = genius.search_song(text, artist='', get_full_info=False)
    if not song:
        update.message.reply_text("Unable to find lyrics for the given song.")
    else:
        lyrics = song.lyrics
        song_length = len(lyrics)
        count = 0
        try:
            while song_length > 4096:
                update.message.reply_text(lyrics[:4096])
                song_length -= 4096
                count+=1
            update.message.reply_text(lyrics[4096*count:])
        except:
            update.message.reply_text("Unable to find lyrics for the given song.")
    update.message.reply_text("Use /help to list available actions.")
    return ConversationHandler.END

@send_typing_action
def imdb_movie_review(update, context):
    '''get movie review'''
    query = update.message.text
    query = query.replace(' ', '+')
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {'query': query, 'api_key': MOVIE_TOKEN}
    req = requests.get(url, params=params)
    if req.status_code == 200:
        try:
            data = req.json()['results'][0]
        except:
            update.message.reply_text("Couldn't find the given movie.")
            update.message.reply_text("Use /help to list available actions.")
            return ConversationHandler.END

        movie_to_str(update, context, data) # formulates string from given data and messages to user
    else:
        update.message.reply_text("Couldn't find the given movie.")
    update.message.reply_text("Use /help to list available actions.")
    return ConversationHandler.END

@send_typing_action
def url_shortener(update, context):
    '''shorten the url'''
    text = update.message.text
    shortener = Shortener() #create shortener object
    try:
        short_url = shortener.tinyurl.short(text)
    except:
        update.message.reply_text("Cannot shorten the given url.")
        update.message.reply_text("Use /help to list available actions.")
        return ConversationHandler.END

    update.message.reply_text(short_url)
    update.message.reply_text("Use /help to list available actions.")
    return ConversationHandler.END

@send_typing_action
def retrieve_weather_info(update, context):
    '''get weather info'''
    text = update.message.text
    text = text.replace(' ', '+')
    params = {'q': text, 'appid': WEATHER_TOKEN}
    req = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params)
    if req.status_code == 200:
        data = req.json()
        try:
            weather = data['weather'][0]['description']
            celsius = convert_to_celsius(data['main']['temp'])
        except:
            update.message.reply_text("Couldn't fetch weather for the given city.")
            update.message.reply_text("Use /help to list available actions.")
            return ConversationHandler.END
        update.message.reply_text("Description: <strong>{}</strong>\nTemperature: <strong>{:.2f} celsius</strong>".format(weather, celsius), parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text("Couldn't fetch weather for given city")
    update.message.reply_text("Use /help to list available actions.")
    return ConversationHandler.END

@send_typing_action
def word_meaning(update, context):
    '''get words meaning'''
    text = update.message.text
    dictionary = PyDictionary()
    try:
        meanings = dictionary.meaning(text)
    except:
        update.message.reply_text("Unable to find meaning for the given word.")
        return ConversationHandler.END

    result = ""
    try:
        for key, items in meanings.items():
            for item in items:
                result += f"<strong>{text}</strong>({key}): {item}\n"
        if result:
            update.message.reply_text(result, parse_mode=ParseMode.HTML)
    except:
        update.message.reply_text("Unable to find meaning for the given word.")
    update.message.reply_text("Use /help to list available actions.")
    return ConversationHandler.END

@send_typing_action
def handle_poll(update, context):
    '''handle the poll'''
    """On receiving polls, reply to it by a closed poll copying the received poll"""
    actual_poll = update.effective_message.poll
    update.effective_message.reply_poll(
        question=actual_poll.question,
        options=[o.text for o in actual_poll.options],
        is_closed=False,
        reply_markup=ReplyKeyboardRemove(),
    )
    update.message.reply_text("Use /help to list available actions.")
    return ConversationHandler.END
