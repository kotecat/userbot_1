from pyrogram import types, filters
from loader import bot
from scripts import Field, FieldRow
from loader import balda


@bot.on_message(filters.me & filters.command(["balda"], ["!", "/", "."]), group=0)
async def balda_cheat(_, message: types.Message):
    return
    print("ddd")
    field = Field([
        FieldRow(["", "", ""]),
        FieldRow(["х", "у", "й"]),
        FieldRow(["", "", ""])
    ])

    await message.reply(str(await balda.get_words(field))[:1023])
