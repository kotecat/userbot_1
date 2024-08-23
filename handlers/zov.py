from pyrogram import types, filters
from loader import bot
from simple_filters import app_admins_filter
from utils.text_coder import (
    text_to_bits, bits_to_code,
    code_to_bits, bits_to_text
)
from random import randint


@bot.on_message(app_admins_filter & ~filters.media & filters.command(["ze"], ["/", "!", "."]), group=10)
async def on_ze_command(_, message: types.Message):
    if len(message.command) == 1:
        await message.delete()

    input_text = message.text.split(" ", maxsplit=1)[-1]

    code = bits_to_code(text_to_bits(input_text))
    result = ""
    for c in code:
        result += c.lower() if randint(0, 1) else c.upper()

    result = f"_{result}_"

    if len(result) > 4093:
        result = result[:4093] + "..."

    await message.edit_text(result)


@bot.on_message(app_admins_filter & ~filters.media & filters.command(["zd"], ["/", "!", "."]), group=10)
async def on_zd_command(_, message: types.Message):
    if len(message.command) == 1:
        await message.delete()

    input_text = message.text.split(" ", maxsplit=1)[-1].lower().strip("_")
    input_text = input_text.replace("\n", "")

    text = bits_to_text(code_to_bits(input_text))
    result = text

    if len(result) > 4093:
        result = result[:4093] + "..."

    await message.edit_text(result)
