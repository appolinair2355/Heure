import os
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 10000))

subscribers = set()

async def send_time(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now().strftime("%H:%M:%S")
    for chat_id in subscribers:
        await context.bot.send_message(chat_id=chat_id, text=f"Heure actuelle : {now}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    subscribers.add(chat_id)
    await update.message.reply_text("⏰ Tu recevras l'heure toutes les 2 minutes.")
    job_name = f"time_{chat_id}"
    if not context.job_queue.get_jobs_by_name(job_name):
        context.job_queue.run_repeating(send_time, interval=120, first=0, name=job_name)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    await app.bot.set_webhook(WEBHOOK_URL)
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
    )

# ✅ Ne pas utiliser asyncio.run() ici
if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
