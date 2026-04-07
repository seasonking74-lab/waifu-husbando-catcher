import random
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, filters
from shivu import application, collection, user_collection, group_totals

last_characters = {}
message_counts = {}

async def message_counter(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not update.message or not update.message.text: return
    
    message_counts[chat_id] = message_counts.get(chat_id, 0) + 1
    if message_counts[chat_id] >= 50:
        message_counts[chat_id] = 0
        all_chars = await collection.find({}).to_list(length=None)
        if not all_chars: return
        
        char = random.choice(all_chars)
        last_characters[chat_id] = char
        await context.bot.send_photo(
            chat_id=chat_id, photo=char['img_url'],
            caption=f"❄️ **𝐀 𝐍𝐄𝐖 𝐂𝐇𝐀𝐑𝐀𝐂𝐓𝐄𝐑 𝐀𝐏𝐏𝐄𝐀𝐑𝐄𝐃!**\n━━━━━━━━━━━━━━━━━━━━\n💎 **Rarity:** {char['rarity']}\n\n𝗨𝘀𝗲 `/hunt [name]` 𝘁𝗼 𝗰𝗮𝘁𝗰𝗵! ⛄️"
        )

async def hunt(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id not in last_characters: return
    
    guess = " ".join(context.args).lower()
    char = last_characters[chat_id]
    
    if guess == char['name'].lower():
        user_id = update.effective_user.id
        await user_collection.update_one({'id': user_id}, {'$push': {'characters': char}, '$set': {'first_name': update.effective_user.first_name}}, upsert=True)
        await group_totals.update_one({'group_id': chat_id}, {'$inc': {'count': 1}, '$set': {'group_name': update.effective_chat.title}}, upsert=True)
        del last_characters[chat_id]
        await update.message.reply_text(f"✅ **CORRECT!** {update.effective_user.first_name} caught **{char['name']}**!")
    else:
        await update.message.reply_text("❌ Wrong name! Try again.")

application.add_handler(CommandHandler(["hunt", "grab"], hunt))
application.add_handler(MessageHandler(filters.ChatType.GROUPS, message_counter))
