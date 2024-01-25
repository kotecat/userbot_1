from pyrogram import Client, enums
from config import Config
from scripts import BaldaApi


balda = BaldaApi()
bot = Client(
    "fonk",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    parse_mode=enums.ParseMode.HTML
)