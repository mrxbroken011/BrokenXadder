import logging
import os
from functools import wraps
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from telegram.ext import MessageHandler, Filters
from telegram.utils.request import Request


# Load environment variables from Heroku config vars
BOT_TOKEN = os.getenv('BOT_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID'))  # Make sure OWNER_ID is set in the environment variables

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def owner_only(func):
    @wraps(func)
    def wrapped(update: Update, context: CallbackContext, *args, **kwargs):
        if update.message.from_user.id != OWNER_ID:
            update.message.reply_text('You are not authorized to use this bot.')
            return
        return func(update, context, *args, **kwargs)
    return wrapped

@owner_only
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am Mr Broken's bot. Use /add <user_id> to add a member to the group.')

@owner_only
def add_member(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type != 'private':
        update.message.reply_text('This command can only be used in private chat.')
        return
    
    if len(context.args) != 2:
        update.message.reply_text('Usage: /add <user_id> <group_id>')
        return
    
    user_id = context.args[0]
    group_id = context.args[1]
    
    try:
        context.bot.add_chat_members(chat_id=group_id, user_ids=[user_id])
        update.message.reply_text(f'Successfully added user {user_id} to group {group_id}.')
    except Exception as e:
        update.message.reply_text(f'Failed to add user: {e}')
        logger.error(f'Error adding user: {e}')

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add", add_member))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT.
    updater.idle()

if __name__ == '__main__':
    main()
