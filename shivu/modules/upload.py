import asyncio, random
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application, collection, Config, RARITY_MAP

async def gupload(update: Update, context: CallbackContext):
    if update.effective_user.id != Config.OWNER_ID: return
    if not update.message.photo: return
    
    p_msg = await update.message.reply_text("`<PROCESSING>....`", parse_mode="MarkdownV2")
    await asyncio.sleep(1)

    try:
        args = update.message.caption.replace("/gupload ", "").split()
        name, anime, r_id = args[0].replace("-", " "), args[1].replace("-", " "), args[2]
        r_name = RARITY_MAP.get(r_id, "⚪️ Common")
        
        char_id = str(random.randint(1000, 9999))
        await collection.insert_one({"id": char_id, "name": name, "anime": anime, "rarity": r_name, "img_url": update.message.photo[-1].file_id})
        await p_msg.edit_text(f"➲ **ADDED BY»** —{update.effective_user.first_name}\n➥ **ID:** {char_id}\n➥ **Rarity:** {r_name}")
    except:
        await p_msg.edit_text("❌ **Format:** `/gupload Name-Anime-RarityID` (In Photo Caption)")

application.add_handler(CommandHandler("gupload", gupload))
