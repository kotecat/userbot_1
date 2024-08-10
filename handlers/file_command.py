from pyrogram import types, filters
from pyrogram.file_id import FileId, FileType
# from pyrogram.errors.exceptions.bad_request_400 import
from loader import bot
from simple_filters import app_admins_filter


@bot.on_message(app_admins_filter & ~filters.media & filters.command(["file"], ["/", "!", "."]), group=1)
async def on_file_command(_, message: types.Message):
    msg = message.reply_to_message or message

    file_id = message.text.strip().split()[-1]

    try:
        file = FileId.decode(file_id)
        file_type = file.file_type
    except:
        return

    if "-info" in message.text:
        await msg.reply(file.__dict__)
        return

    try:
        if file_type == FileType.AUDIO:
            await msg.reply_audio(file_id)
        elif file_type == FileType.PHOTO:
            await msg.reply_photo(file_id)
        elif file_type == FileType.STICKER:
            await msg.reply_sticker(file_id)
        elif file_type == FileType.VIDEO:
            await msg.reply_video(file_id)
        elif file_type == FileType.VIDEO_NOTE:
            await msg.reply_video_note(file_id)
        elif file_type == FileType.VOICE:
            await msg.reply_voice(file_id)
        elif file_type == FileType.DOCUMENT:
            await msg.reply_document(file_id)
    except Exception as e:
        await msg.reply(f"FILE_TYPE: {file_type}\nerror: {e}")


