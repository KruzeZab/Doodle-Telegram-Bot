import os
from telegram import ParseMode
from telegram.ext import (
    Updater, 
    CommandHandler, 
    MessageHandler,
    ConversationHandler, 
    Filters
)
from generics.intimacy_bot import intimacy_quiz #intimac quiz
from generics.meta import BOT_TOKEN, MIN_CHOICE, MAX_CHOICE, help_text #import tokens and ranges
# Conversation states
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
#ask for extra information before passing to handlers
from generics.choice_input import (
    youtube_input,
    wikipedia_input,
    song_lyrics_input,
    movie_review_input,
    url_shortener_input,
    weather_input,
    poll_input,
    dictionary_input,
)
#state methods handlers
from generics.action_handler import (
    youtube_downloader,
    wikipedia_summary,
    send_random_joke,
    retrieve_song_lyrics,
    imdb_movie_review,
    url_shortener,
    retrieve_weather_info,
    handle_poll,
    word_meaning
)
#unexpected response handlers
from generics.handlers import (
    handle_wikipedia,
    handle_song_lyrics,
    handle_imdb_movie_review,
    handle_weather_info,
    handle_url_shortener,
    handle_bad_poll,
    handle_dictionary,
    handle_youtube,
)
from generics.typing_action import send_typing_action 

PORT = int(os.environ.get('PORT', 5000))

@send_typing_action
def help(update, context):
    '''send help actions text on /help'''
    update.message.reply_text("These are the actions you can perform: ")
    update.message.reply_text(help_text)

@send_typing_action
def start(update, context):
    '''Greet user on /start'''
    user = update.message.from_user
    update.message.reply_text(
        f"Hi <strong>{user.first_name} {user.last_name}</strong>. I'm `Doodle Bot`. 🤗",
        parse_mode=ParseMode.HTML
    )
    update.message.reply_text("Use /help to list available actions.")
    update.message.reply_text(
        f"Please choose a number for corresponding action. ({MIN_CHOICE} - {MAX_CHOICE})"
    )
    update.message.reply_text(help_text)

@send_typing_action
def inappropriate_action(update, context):
    '''handle fallback for conversation handler'''
    update.message.reply_text("Inappropriate action.")
    update.message.reply_text(f"Please choose a number for corresponding action. ({MIN_CHOICE} - {MAX_CHOICE})")
    update.message.reply_text(help_text)
    return ConversationHandler.END

@send_typing_action
def stop(update, context):
    '''end the conversation'''
    update.message.reply_text("Stopping Conversation.")
    update.message.reply_text("Use /help to list available actions.")
    return ConversationHandler.END

def main():
    updater = Updater(BOT_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('help', help))

    conv_handler = ConversationHandler(
        entry_points=[
                CommandHandler('start', start),
                MessageHandler(Filters.regex('^1$'), youtube_input),
                MessageHandler(Filters.regex('^2$'), wikipedia_input),
                intimacy_quiz(),
                MessageHandler(Filters.regex('^4$'), send_random_joke),
                MessageHandler(Filters.regex('^5$'), song_lyrics_input),
                MessageHandler(Filters.regex('^6$'), movie_review_input),
                MessageHandler(Filters.regex('^7$'), url_shortener_input),
                MessageHandler(Filters.regex('^8$'), weather_input),
                MessageHandler(Filters.regex('^9$'), dictionary_input),
                MessageHandler(Filters.regex('^10$'), poll_input),
                MessageHandler(Filters.all, inappropriate_action),
            ],
            states={
                YOUTUBE: [
                    MessageHandler(Filters.text & ~Filters.command, youtube_downloader),
                    MessageHandler(~Filters.text & ~Filters.command, handle_youtube),
                ],
                WIKIPEDIA: [
                    MessageHandler(Filters.text & ~Filters.command, wikipedia_summary),
                    MessageHandler(~Filters.text & ~Filters.command, handle_wikipedia),
                ],
                LYRICS: [
                    MessageHandler(Filters.text & ~Filters.command, retrieve_song_lyrics),
                    MessageHandler(~Filters.text & ~Filters.command, handle_song_lyrics),
                ],
                URL: [
                    MessageHandler(Filters.text & ~Filters.command, url_shortener),
                    MessageHandler(~Filters.text & ~Filters.command, handle_url_shortener),
                ],
                MOVIE: [
                    MessageHandler(Filters.text & ~Filters.command, imdb_movie_review),
                    MessageHandler(~Filters.text & ~Filters.command, handle_imdb_movie_review),
                ],
                WEATHER: [
                    MessageHandler(Filters.text & ~Filters.command, retrieve_weather_info),
                    MessageHandler(~Filters.text & ~Filters.command, handle_weather_info),
                ],
                DICTIONARY: [
                    MessageHandler(Filters.text & ~Filters.command, word_meaning),
                    MessageHandler(~Filters.text & ~Filters.command, handle_dictionary)
                ],
                POLL: [
                    MessageHandler(Filters.poll, handle_poll),
                    MessageHandler(~Filters.poll, handle_bad_poll)
                ],
            },
        fallbacks=[
            CommandHandler('stop', stop),
            MessageHandler(Filters.all & ~Filters.command, inappropriate_action),
        ],
    )

    dp.add_handler(conv_handler)

    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=BOT_TOKEN)
    updater.bot.setWebhook('https://doodletelegrambot.herokuapp.com/' + BOT_TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()

