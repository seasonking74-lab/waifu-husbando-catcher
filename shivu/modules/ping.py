import time
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from shivu import application

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    message = await update.message.reply_text("❄️ Pinging...")
    end_time = time.time()
    ms = (end_time - start_time) * 1000
    await message.edit_text(f"⛄️ **Pong!**\n⏱ Speed: `{int(ms)}ms`")

application.add_handler(CommandHandler("ping", ping))
