import asyncio
import os
import random
import time
from html import escape
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, filters
from shivu import application, shivuu, collection, user_collection, user_totals_collection, LOGGER, OWNER_ID, RARITY_MAP

# --- 1. RENDER WEB SERVER (Keeping Bot Alive) ---
async def handle(request): return web.Response(text="Gʀᴀsᴘ Cʜᴀʀᴀᴄᴛᴇʀs Is Lɪᴠᴇ! ⛄️")
async def start_server():
    app = web.Application(); app.router.add_get('/', handle)
    runner = web.AppRunner(app); await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    await web.TCPSite(runner, '0.0.0.0', port).start()

# Game States
last_characters = {}
message_counts = {}

# --- 2. ADMIN COMMAND: /gupload ---
async def gupload(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID: return
    if not update.message.photo: return
    
    p_msg = await update.message.reply_text("`<PROCESSING>....`", parse_mode="MarkdownV2")
    try:
        args = update.message.caption.replace("/gupload ", "").split()
        name, anime, r_id = args[0].replace("-", " "), args[1].replace("-", " "), args[2]
        r_name = RARITY_MAP.get(r_id, "⚪️ Common")
        
        char_id = str(random.randint(1000, 9999))
        await collection.insert_one({
            "id": char_id, "name": name, "anime": anime, "rarity": r_name, "img_url": update.message.photo[-1].file_id
        })
        await p_msg.edit_text(f"➲ ADDED BY» —{update.effective_user.first_name}\n➥ Character ID: {char_id}\n➥ Rarity: {r_name}")
    except: await p_msg.edit_text("❌ Format: `/gupload Name Anime RarityID`")

# --- 3. AUTO SPAWN LOGIC (Message Counter) ---
async def message_counter(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not update.message or not update.message.text: return
    
    message_counts[chat_id] = message_counts.get(chat_id, 0) + 1
    if message_counts[chat_id] >= 50: # Har 50 message par spawn
        message_counts[chat_id] = 0
        all_chars = await collection.find({}).to_list(length=None)
        if not all_chars: return
        
        char = random.choice(all_chars)
        last_characters[chat_id] = char
        await context.bot.send_photo(
            chat_id=chat_id, photo=char['img_url'],
            caption=f"🌕 **𝐀 𝐍𝐄𝐖 𝐂𝐇𝐀𝐑𝐀𝐂𝐓𝐄𝐑 𝐀𝐏𝐏𝐄𝐀𝐑𝐄𝐃**\n\n💎 Rarity: {char['rarity']}\n\nUse `/hunt [name]` to catch! ⛄️"
        )

# --- 4. HUNT COMMAND ---
async def hunt(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id not in last_characters: return
    
    guess = " ".join(context.args).lower()
    char = last_characters[chat_id]
    
    if guess == char['name'].lower():
        user_id = update.effective_user.id
        await user_collection.update_one(
            {'id': user_id},
            {'$push': {'characters': char}, '$set': {'first_name': update.effective_user.first_name}},
            upsert=True
        )
        del last_characters[chat_id]
        await update.message.reply_text(f"✅ **CORRECT!** {update.effective_user.first_name} caught **{char['name']}**!")
    else:
        await update.message.reply_text("❌ Galat naam! Fir se koshish karein.")

# --- 5. MAIN STARTUP ---
def main():
    # Handlers add karein
    application.add_handler(CommandHandler("gupload", gupload))
    application.add_handler(CommandHandler(["hunt", "grab", "guess"], hunt))
    application.add_handler(MessageHandler(filters.ChatType.GROUPS, message_counter))
    
    # Start all services
    loop = asyncio.get_event_loop()
    loop.create_task(start_server()) # Render keep-alive
    
    shivuu.start() # Pyrogram start
    LOGGER.info("Gʀᴀsᴘ Cʜᴀʀᴀᴄᴛᴇʀs Pʀᴏ Is Lɪᴠᴇ!")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
