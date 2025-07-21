import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

user_jobs = {}  # Pour suivre les utilisateurs actifs

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text("⏰ Le bot va vous envoyer l'heure toutes les 2 minutes.")
    
    # Démarre le job répétitif
    job = context.application.job_queue.run_repeating(send_time, interval=120, first=0, chat_id=chat_id)
    user_jobs[chat_id] = job

async def send_time(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now().strftime('%H:%M:%S')
    await context.bot.send_message(chat_id=context.job.chat_id, text=f"🕒 Il est {now}")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    job = user_jobs.get(chat_id)
    if job:
        job.schedule_removal()
        await update.message.reply_text("⛔️ Arrêt de l'envoi de l'heure.")
    else:
        await update.message.reply_text("Aucun envoi actif.")
        
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()
