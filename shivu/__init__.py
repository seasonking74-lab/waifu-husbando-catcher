import logging
from telegram.ext import ApplicationBuilder
from motor.motor_asyncio import AsyncIOMotorClient

# Logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CONFIG ---
TOKEN = "8568309223:AAHWam_aBpk1K6pD29bf75nzwbEyoSFqxBU"
MONGO_URL = "mongodb+srv://season74_db_user:pass%401220@cluster0.nuxjsu4.mongodb.net/?retryWrites=true&w=majority"
OWNER_ID = 8629880263

# DB Connection
client = AsyncIOMotorClient(MONGO_URL)
db = client.grasp_pro
chars_col = db.characters
users_col = db.users

# Application
application = ApplicationBuilder().token(TOKEN).build()
