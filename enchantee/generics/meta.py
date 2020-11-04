'''
contains meta data for
- Bot Token, 
- Min Choice Range, 
- Max Choice Range,
'''

import os

BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
LYRICS_TOKEN = os.environ.get('GENIUS_LYRICS_TOKEN')
MOVIE_TOKEN = os.environ.get('MOVIE_TOKEN')
WEATHER_TOKEN = os.environ.get('WEATHER_TOKEN')

(
    YOUTUBE, 
    WIKIPEDIA,
    LYRICS,
    MOVIE,
    URL,
    WEATHER,
    DICTIONARY,
    POLL
) = map(chr, range(8))

# USer can select number  from min choice to max choice
MIN_CHOICE = 1 
MAX_CHOICE = 10

#Show this text as Options
help_text = '''\
1 - Youtube Video Downloader ▶️
2 - Wikipeida Summary 📕
3 - Intimacy Quiz - Tell us about yourself ❤️
4 - Send a Joke 😂
5 - Get Song Lyrics 🎶
6 - IMDB Movie Review ⏯
7 - URL Shortener 🔗
8 - Get Current Weather Data 🌦
9 - Dictionary (Word Meaning) 📖
10 - Create a Poll 💈
\
'''
