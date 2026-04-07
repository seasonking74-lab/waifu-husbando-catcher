import logging
from telegram.ext import Application
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client

# 1. Logging Setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
LOGGER = logging.getLogger(__name__)

# --- 2. CONFIG SETTINGS ---
TOKEN = "7544040994:AAEqP_G1S4-XXXXXXXX" # <--- APNA TOKEN
MONGO_URL = "mongodb+srv://season74_db_user:pass%401220@cluster0.nuxjsu4.mongodb.net/?retryWrites=true&w=majority"
OWNER_ID = 8629880263
api_id = 34967775
api_hash = "e6e5dfae5327f90410863f93d8ced26b"

# --- 3. DATABASE CONNECTION ---
client = AsyncIOMotorClient(MONGO_URL)
db = client['Grasp_Pro_DB']

collection = db['anime_characters'] # Uploaded Characters
user_collection = db["user_collection_lmao"]
user_totals_collection = db["user_totals_collection"]
sudo_collection = db["sudo_users_list"]

# --- 4. BOT CLIENTS ---
# Python-Telegram-Bot (For Commands)
application = Application.builder().token(TOKEN).build()
# Pyrogram (For Shivu session logic)
shivuu = Client("shivu_session", api_id, api_hash, bot_token=TOKEN)

# Rarity Map
RARITY_MAP = {rarity_map = {
    1: "⚪️ Common",
    2: "🟣 Rare",
    3: "🟡 Legendary",      
    4: "🟢 Medium",  
    5: "💮 Special Edition", 
    6: "🔮 Limited Edition", 
    7: "💸 Premium Edition", 
    8: "🌤 Summer",
    9: "🎐 Celestial", 
    10: "❄️ Winter", 
    11: "💝 Valentine", 
    12: "🎃 Halloween", 
    13: "🎄 Christmas Special", 
    14: "🪐 Omniversal", 
    15: "🎭 Cosplay Master 🎭",
    16: "🧧 Events",
    17: "🍑 Echhi",
    18: "🎗️ AMV Edition",
    19: "🌟 Luminous",
    22: "🍭 Winter event",
    23: "🌈 Holi Edition",
}
}
