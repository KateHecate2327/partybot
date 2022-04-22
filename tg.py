import os
from telegram import Update
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater

from PartyBot import PARTY_INTENT, get_answer
from parties import Party, Parties

from dotenv import load_dotenv

# Читаем конфигурацию
load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

updater = Updater( token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
parties = Parties()


def echo(update: Update, context: CallbackContext):
    response = get_answer(update.message.text)
    if not response:
        return

    chat_id=update.effective_chat.id

    text, intent = response
    if intent != PARTY_INTENT:
        context.bot.send_message(chat_id=chat_id, text=text)

    print(update.message)


echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


updater.start_polling()
updater.idle()
