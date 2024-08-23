from pyrogram import types, filters
from loader import bot
from simple_filters import app_admins_filter
from random import randint


@bot.on_message(app_admins_filter & ~filters.media, group=11)
async def on_toad_delete(_, message: types.Message):
    if message.text.startswith("@toadbot "):
        await message.delete()
