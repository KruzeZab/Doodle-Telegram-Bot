from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, Filters

(
    NAME,
    GENDER, 
    AGE, 
    PHOTO, 
    SKIP_PHOTO,
    ADDRESS, 
    BIO
) = map(chr, range(7))


def _facts_to_str(user_data):
    if not user_data:
        return 
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])

def start(update, context):
    '''ask name'''
    update.message.reply_text(
        "Hi! I am professor Bot. Let's have a simple chat so I can know you better. \n"
        "Send /cancel to stop at anytime."
    )
    update.message.reply_text("What is your name?")
    return NAME

def name(update, context):
    '''ask gender'''
    context.user_data['Name'] = update.message.text
    reply_keyboard = [['Boy', 'Girl', 'Other']]
    update.message.reply_text("That's a nice name.")
    update.message.reply_text(
        "Are you a boy or a girl?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, 
            one_time_keyboard=True, 
            resize_keyboard=True
        )
    )
    return GENDER

def gender(update, context):
    '''ask age'''
    context.user_data['Gender'] = update.message.text
    update.message.reply_text("Awesome!")
    update.message.reply_text("How old are you?")
    return AGE


def age(update, context):
    '''ask photo'''
    context.user_data['Gender'] = update.message.text
    update.message.reply_text(
        "I see. Please send me a photo of yourself\n"
        "Send /skip to skip.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return PHOTO



def photo(update, context):
    context.user_data['Photo'] = 'Provided'
    update.message.reply_text("You look awesome!")
    update.message.reply_text("Now please tell me your address")
    return ADDRESS

def skip_photo(update, context):
    '''skip photo'''
    context.user_data['Photo'] = 'Not Provided'
    update.message.reply_text("Ok, Fine.")
    update.message.reply_text("Atleast, tell me your address.")
    return ADDRESS

def address(update, context):
    '''ask bio'''
    context.user_data['Address'] = update.message.text
    update.message.reply_text("Great!")
    update.message.reply_text("Now, tell me something about yourself that I need to know.")
    return BIO

def bio(update, context):
    '''end convo'''
    context.user_data['Bio'] = update.message.text
    update.message.reply_text("Great! It was nice talking to you. You are an interesting person.")
    update.message.reply_text("This is what information you gave me so far:")
    update.message.reply_text(_facts_to_str(context.user_data))
    update.message.reply_text("Use /help to list available actions.")
    return ConversationHandler.END

def cancel(update, context):
    '''cancel intimacy convo'''
    update.message.reply_text("Great! It was nice talking to you.")
    if context.user_data:
        update.message.reply_text("This is what information you gave me so far:")
        update.message.reply_text(_facts_to_str(context.user_data))
    update.message.reply_text("Use /help to list available actions.")
    return ConversationHandler.END

def inappropriate_action(update, context):
    '''handle fallback for conversation handler'''
    update.message.reply_text("Please select an appropriate action.")
    update.message.reply_text("Use /help to list available actions.")
    return ConversationHandler.END

#Intimacy quiz handlers
def error_name(update, context):
    '''handle unexpected response'''
    update.message.reply_text("Please enter a name.")
    return NAME

def error_gender(update, context):
    '''handle unexpected response'''
    update.message.reply_text("Please select your gender.")
    return GENDER

def error_age(update, context):
    '''handle unexpected response'''
    update.message.reply_text("Please enter your age.")
    return AGE

def error_photo(update, context):
    '''handle unexpected response'''
    update.message.reply_text("Please send your photo.")
    return PHOTO

def error_address(update, context):
    '''handle unexpected response'''
    update.message.reply_text("Please enter your address.")
    return ADDRESS

def error_bio(update, context):
    '''handle unexpected response'''
    update.message.reply_text("Please enter your bio.")
    return BIO

def intimacy_quiz():
    '''has the convo handler for quiz'''
    result = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^3$'), start)],
        states={
            NAME: [
                MessageHandler(Filters.text & ~Filters.command, name),
                MessageHandler(~Filters.text & ~Filters.command, error_name),
            ],
            GENDER: [
                MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender),
                MessageHandler(~Filters.regex('^(Boy|Girl|Other)$') & ~Filters.command, error_gender),
                ],
            AGE: [
                MessageHandler(Filters.regex('^\d+$'), age),
                MessageHandler(Filters.regex('^\D+$'), error_age),
                ],
            PHOTO: [
                MessageHandler(Filters.photo, photo),
                MessageHandler(~Filters.photo & ~Filters.command, error_photo),
                CommandHandler('skip', skip_photo),
            ],
            ADDRESS: [
                MessageHandler(Filters.text & ~Filters.command, address),
                MessageHandler(~Filters.text & ~Filters.command, error_address),
                ],
            BIO: [
                MessageHandler(Filters.text & ~Filters.command, bio),
                MessageHandler(~Filters.text & ~Filters.command, error_bio),
            ]
        },
        fallbacks=[
            CommandHandler('cancel', cancel),
            MessageHandler(Filters.all, inappropriate_action)
        ],
    )   
    return result
