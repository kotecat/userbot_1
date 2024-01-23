from pyrogram import types, filters
from loader import bot
from simple_filters import app_admins_filter


@bot.on_message(app_admins_filter & filters.private, group=-1)
async def try_eval(_, message: types.Message):
    text = message.text
    msg = message
    reply = message.reply_to_message

    try:
        result = eval(text)
    except Exception as e:
        pass
    else:
        await message.edit_text(f"{text}\n<b>result</b>: <code>{result}</code>")

    message.continue_propagation()
