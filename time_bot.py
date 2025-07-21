import os
import threading
import time
from datetime import datetime
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

user_active = {}

def send_time(chat_id):
    while user_active.get(chat_id, False):
        now = datetime.now().strftime("%H:%M:%S")
        bot.send_message(chat_id=chat_id, text=f"Heure actuelle : {now}")
        time.sleep(120)  # 2 minutes

def start(update, context):
    chat_id = update.effective_chat.id
    if not user_active.get(chat_id):
        user_active[chat_id] = True
        threading.Thread(target=send_time, args=(chat_id,), daemon=True).start()
        context.bot.send_message(chat_id=chat_id, text="🔔 Envoi de l'heure toutes les 2 minutes activé.")
    else:
        context.bot.send_message(chat_id=chat_id, text="⏱️ Déjà en cours.")

dispatcher.add_handler(CommandHandler("start", start))

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

@app.route("/", methods=["GET"])
def home():
    return "Bot Telegram Heure - Actif"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
