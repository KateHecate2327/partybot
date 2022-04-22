import os
from telegram import Update
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater

from PartyBot import get_answer

from dotenv import load_dotenv

# Читаем конфигурацию
load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

updater = Updater(
    token=BOT_TOKEN, use_context=True
)
dispatcher = updater.dispatcher


def echo(update: Update, context: CallbackContext):
    text = update.message.text
    response, intent = get_answer(text)
    print(intent)
    if response:
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)


echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


updater.start_polling()
updater.idle()
