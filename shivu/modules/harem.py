import math
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from shivu import application, user_collection

async def harem(update: Update, context: CallbackContext, page=0):
    user_id = update.effective_user.id
    user = await user_collection.find_one({'id': user_id})
    
    if not user or not user.get('characters'):
        return await (update.message.reply_text("Your collection is empty!") if update.message else update.callback_query.answer("Empty!"))

    chars = user['characters']
    total_pages = math.ceil(len(chars) / 10)
    
    text = f"🏯 **{update.effective_user.first_name}'s Harem** (Page {page+1}/{total_pages})\n\n"
    for c in chars[page*10 : (page+1)*10]:
        text += f"❄️ `{c['id']}` **{c['name']}**\n"
    
    buttons = []
    if page > 0: buttons.append(InlineKeyboardButton("⬅️", callback_data=f"harem_{page-1}"))
    if page < total_pages - 1: buttons.append(InlineKeyboardButton("➡️", callback_data=f"harem_{page+1}"))
    
    kb = InlineKeyboardMarkup([buttons]) if buttons else None
    if update.message:
        await update.message.reply_text(text, reply_markup=kb, parse_mode="Markdown")
    else:
        await update.callback_query.edit_message_text(text, reply_markup=kb, parse_mode="Markdown")

async def harem_callback(update: Update, context: CallbackContext):
    page = int(update.callback_query.data.split("_")[1])
    await harem(update, context, page)

application.add_handler(CommandHandler(["harem", "collection"], harem))
application.add_handler(CallbackQueryHandler(harem_callback, pattern="^harem_"))
