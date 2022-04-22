import datetime
import os
import time
from telegram import Update, Bot
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater
from multiprocessing import Process
import shelve

from PartyBot import PARTY_INTENT, get_answer
from parties import Parties

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
parties = Parties()

try:
    os.remove("partystorage.bak")
    os.remove("partystorage.dat")
    os.remove("partystorage.dir")
except:
    pass

def handle(update: Update, context: CallbackContext):
    response = get_answer(update.message.text)
    if not response:
        return

    chat_id=update.effective_chat.id

    text, intent = response
    if intent != PARTY_INTENT:
        context.bot.send_message(chat_id=chat_id, text=text)
        return

    party = parties.get_party() or parties.new_party(chat_id=chat_id)
    if not party:
        return

    party.add_participant(update.message.from_user.username)

    db = shelve.open("partystorage")
    db["parties"] = parties
    db.close()

echo_handler = MessageHandler(Filters.text, handle)
dispatcher.add_handler(echo_handler)


def start_polling():
    updater.start_polling()
    updater.idle()


def start_printing():
    while True:
        now = datetime.datetime.utcnow()
        ufa_21_00 = 16
        ufa_22_00 = 17

        if now.hour < 11 or now.hour > 12:
            print("еще рано")
            time.sleep(60*60)
            continue

        db = shelve.open("partystorage")
        parties = db.get("parties")
        db.close()
        if parties:
            party = parties.get_party()

            if party:
                Bot(BOT_TOKEN).send_message(chat_id=party.chat_id, text=party.mention())
                time.sleep(60*60)
                continue

        time.sleep(5)

p1 = Process(target=start_polling).start()
p2 = Process(target=start_printing).start()