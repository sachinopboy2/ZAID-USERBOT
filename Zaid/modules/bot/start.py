import os
import re
import asyncio
import time
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Zaid import app, API_ID, API_HASH
from config import OWNER_ID, ALIVE_PIC

# --- Dashboard Design ---
START_IMG = ALIVE_PIC 

START_TEXT = (
    "<b>╭━━━〔 ɴᴏʙɪᴛᴀ ᴜꜱᴇʀʙᴏᴛ ᴀꜱꜱɪꜱᴛᴀɴᴛ 〕━━━┈⊷</b>\n"
    "<b>┃</b>\n"
    "<b>┃ 👤 ᴍᴀsᴛᴇʀ:</b> <a href='tg://user?id={user_id}'>{first_name}</a>\n"
    "<b>┃ 🤖 sᴛᴀᴛᴜs:</b> <code>ᴀʟɪᴠᴇ & ʀᴇᴀᴅʏ</code>\n"
    "<b>┃ ⚡ ᴘᴏᴡᴇʀ:</b> <code>ɴᴏʙɪ-ᴠ2.1</code>\n"
    "<b>┃</b>\n"
    "<b>┣━━━〔 ᴄʟᴏɴᴇ ꜱʏꜱᴛᴇᴍ 〕━━━┈⊷</b>\n"
    "<b>┃</b>\n"
    "<b>┃ 🌀 ᴅᴇꜱᴄ:</b> ʜᴏꜱᴛ ʏᴏᴜʀ ᴏᴛʜᴇʀ ᴘʏʀᴏɢʀᴀᴍ ꜱᴇꜱꜱɪᴏɴꜱ.\n"
    "<b>┃ 🛠 ᴜꜱᴀɢᴇ:</b> <code>/clone [ꜱᴛʀɪɴɢ_ꜱᴇꜱꜱɪᴏɴ]</code>\n"
    "<b>┃</b>\n"
    "<b>┣━━━〔 ꜱʏꜱᴛᴇᴍ ᴍᴇɴᴜ 〕━━━┈⊷</b>\n"
    "<b>┃</b>\n"
    "<b>┃ ‣ ᴜᴘᴅᴀᴛᴇ:</b> <code>.update deploy</code>\n"
    "<b>┃ ‣ ʀᴇꜱᴛᴀʀᴛ:</b> <code>.restart</code>\n"
    "<b>┃</b>\n"
    "<b>┣━━━〔 ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ 〕━━━┈⊷</b>\n"
    "<b>┃</b>\n"
    "<b>┃ ‣ ᴏᴡɴᴇʀ:</b> @room_cut\n"
    "<b>┃ ‣ ᴄʜᴀɴɴᴇʟ:</b> @faithxxxx\n"
    "<b>┃</b>\n"
    "<b>╰━━━━━━━〔 ɴᴏʙɪᴛᴀ 〕━━━━━━┈⊷</b>"
)

@app.on_message(filters.user(OWNER_ID) & filters.command("start"))
async def hello(client: app, message: Message):
    buttons = [
        [
            InlineKeyboardButton("🌀 ᴄʟᴏɴᴇ ɴᴏᴡ", switch_inline_query_current_chat="/clone "),
            InlineKeyboardButton("🛠 ᴜᴘᴅᴀᴛᴇ", url="https://t.me/faithxxxx"),
        ],
        [
            InlineKeyboardButton("✨ ᴄʜᴀɴɴᴇʟ", url="https://t.me/faithxxxx"),
            InlineKeyboardButton("💎 ꜱᴜᴘᴘᴏʀᴛ", url="https://t.me/nobmz"),
        ],
        [
            InlineKeyboardButton("👤 ᴏᴡɴᴇʀ", url="https://t.me/room_cut"),
            InlineKeyboardButton("📂 ꜱᴏᴜʀᴄᴇ", url="https://github.com/sachinopboy2/ZAID-USERBOT"),
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await client.send_photo(
        chat_id=message.chat.id, 
        photo=START_IMG, 
        caption=START_TEXT.format(
            user_id=message.from_user.id, 
            first_name=message.from_user.first_name
        ), 
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML
    )

@app.on_message(filters.user(OWNER_ID) & filters.command("clone"))
async def clone(bot: app, msg: Message):
    if len(msg.command) < 2:
        return await msg.reply("<b>❌ Usage:</b>\n<code>/clone [your_string_session]</code>")
    
    phone = msg.command[1]
    text = await msg.reply("<code>⌛ Booting Your Client... Please Wait.</code>")
    
    try:
        # Unique name for each session to avoid database lock errors
        client = Client(
            name=f"Nobita_{msg.from_user.id}", 
            api_id=API_ID, 
            api_hash=API_HASH, 
            session_string=phone, 
            plugins=dict(root="Zaid/modules")
        )
        await client.start()
        user = await client.get_me()
        await text.edit(f"<b>✅ Client Successfully Started!</b>\n\n<b>👤 User:</b> {user.first_name}\n<b>🆔 ID:</b> <code>{user.id}</code>")
    except Exception as e:
        await msg.reply(f"<b>❌ ERROR:</b>\n<code>{str(e)}</code>\n\nPress /start to try again.")
