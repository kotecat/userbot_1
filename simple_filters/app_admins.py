from pyrogram import filters
from config import Config


app_admins_filter = filters.user(Config.ME_ID)
