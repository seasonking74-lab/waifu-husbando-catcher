import logging
from telegram.ext import Application
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client
from shivu.config import Config

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# Database
client = AsyncIOMotorClient(Config.MONGO_URL)
db = client['Grasp_Pro_DB']
collection = db['anime_characters']
user_collection = db["user_data"]
group_totals = db["group_totals"]
user_totals = db["user_totals"]

# Bot Clients
application = Application.builder().token(Config.TOKEN).build()
shivuu = Client("shivu_session", Config.API_ID, Config.API_HASH, bot_token=Config.TOKEN)


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
