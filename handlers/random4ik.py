from pyrogram import types, filters
from loader import bot
from simple_filters import app_admins_filter
import random
import re


reg = re.compile(r"(\d+)\D+(\d+)")


@bot.on_message(filters.me & filters.command(["r", "rand", "random"], ["!", "/", "."]), group=5)
async def random_cmd(_, message: types.Message):
    text = message.text or message.caption or ""
    args = " ".join(text.split()[1:])

    m = re.match(reg, args)

    if not m:
        return

    minimum = min(m[1], m[2])
    maximum = max(m[1], m[2])

    if minimum == maximum:
        return

    await message.reply(f"<b>Число: </b> <code>{random.randint(minimum, maximum)}</code>")