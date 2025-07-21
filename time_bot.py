import os
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Dictionnaire pour stocker les utilisateurs à notifier
subscribed_users = set()

# Fonction qui envoie l’heure
async def send_time(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now().strftime("%H:%M:%S")
    for user_id in subscribed_users:
        try:
            await context.bot.send_message(chat_id=user_id, text=f"🕑 Il est {now}")
        except Exception as e:
            print(f"Erreur en envoyant à {user_id}: {e}")

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    subscribed_users.add(user_id)
    await update.message.reply_text("✅ Tu recevras l’heure toutes les 2 minutes.")
    print(f"Utilisateur {user_id} abonné.")

# Lancement
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Ajouter la commande /start
    app.add_handler(CommandHandler("start", start))

    # Planification toutes les 2 minutes
    job_queue = app.job_queue
    job_queue.run_repeating(send_time, interval=120, first=10)

    print("Bot en cours d'exécution...")
    app.run_polling()
