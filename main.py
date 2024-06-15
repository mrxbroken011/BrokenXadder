import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Load environment variables from Heroku config vars
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot. Use /add <user_id> to add a member to the group.')

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
