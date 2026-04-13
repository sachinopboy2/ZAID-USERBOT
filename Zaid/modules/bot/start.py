import os
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from Zaid import app, API_ID, API_HASH
from config import OWNER_ID, ALIVE_PIC, MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB Setup
db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client.Nobita_Bot
approved_users = db.approved_users

async def is_approved(user_id):
    if user_id == OWNER_ID:
        return True
    user = await approved_users.find_one({"user_id": user_id})
    return bool(user)

@app.on_message(filters.command("start"))
async def start_handler(client: app, message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    if not await is_approved(user_id):
        # --- ACCESS DENIED DESIGN ---
        DENIED_TEXT = (
            "<b>╭━━━〔 ᴀᴄᴄᴇꜱꜱ ᴅᴇɴɪᴇᴅ 〕━━━┈⊷</b>\n"
            "<b>┃</b>\n"
            f"<b>┃ 👤 ʜᴇʏ:</b> {first_name}\n"
            "<b>┃ 🚫 sᴛᴀᴛᴜs:</b> <code>ɴᴏᴛ ᴀᴘᴘʀᴏᴠᴇᴅ</code>\n"
            "<b>┃</b>\n"
            "<b>┣━━━〔 ɴᴏᴛɪᴄᴇ 〕━━━┈⊷</b>\n"
            "<b>┃</b>\n"
            "<b>┃</b> <i>ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜsᴇ</i>\n"
            "<b>┃</b> <i>ᴛʜɪs ʙᴏᴛ. ᴘʟᴇᴀsᴇ ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ</i>\n"
            "<b>┃</b> <i>ꜰᴏʀ ʏᴏᴜʀ ᴀᴘᴘʀᴏᴠᴀʟ.</i>\n"
            "<b>┃</b>\n"
            "<b>┃ ‣ ᴀᴅᴍɪɴ:</b> @room_cut\n"
            "<b>┃</b>\n"
            "<b>╰━━━━━━━━━━━━━━━━━━━━┈⊷</b>"
        )
        
        await client.send_message(
            OWNER_ID,
            f"<b>🔔 ɴᴇᴡ ᴀᴄᴄᴇss ʀᴇǫᴜᴇsᴛ!</b>\n\n<b>👤 ᴜsᴇʀ:</b> {first_name}\n<b>🆔 ɪᴅ:</b> <code>{user_id}</code>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"✅ ᴀᴘᴘʀᴏᴠᴇ {first_name}", callback_data=f"approve_{user_id}")]])
        )
        
        return await message.reply_photo(
            photo=ALIVE_PIC,
            caption=DENIED_TEXT,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📩 ʀᴇǫᴜᴇsᴛ ᴀᴘᴘʀᴏᴠᴀʟ", url="https://t.me/room_cut")]])
        )

    # --- BADA START MESSAGE (APPROVED) ---
    START_TEXT = (
        "<b>╭━━━〔 ɴᴏʙɪᴛᴀ ᴜꜱᴇʀʙᴏᴛ ᴠɪᴘ 〕━━━┈⊷</b>\n"
        "<b>┃</b>\n"
        f"<b>┃ 👤 ᴡᴇʟᴄᴏᴍᴇ:</b> <a href='tg://user?id={user_id}'>{first_name}</a>\n"
        "<b>┃ 🤖 sᴛᴀᴛᴜs:</b> <code>ᴀᴘᴘʀᴏᴠᴇᴅ ᴍᴇᴍʙᴇʀ ✅</code>\n"
        "<b>┃ ⚙️ ᴇɴɢɪɴᴇ:</b> <code>ɴᴏʙɪ-ᴠ2.1 ᴘʀᴇᴍɪᴜᴍ</code>\n"
        "<b>┃</b>\n"
        "<b>┣━━━〔 ᴀᴠᴀɪʟᴀʙʟᴇ sᴇʀᴠɪᴄᴇs 〕━━━┈⊷</b>\n"
        "<b>┃</b>\n"
        "<b>┃ 🌀 ᴄʟᴏɴᴇ sʏsᴛᴇᴍ:</b>\n"
        "<b>┃</b> <i>ʜᴏsᴛ ʏᴏᴜʀ ᴏᴛʜᴇʀ ᴘʏʀᴏɢʀᴀᴍ sᴇssɪᴏɴs</i>\n"
        "<b>┃</b> <i>ᴡɪᴛʜ ʜɪɢʜ-sᴘᴇᴇᴅ ᴅᴇᴘʟᴏʏᴍᴇɴᴛ.</i>\n"
        "<b>┃</b> ➔ <code>/clone [ʏᴏᴜʀ_sᴇssɪᴏɴ]</code>\n"
        "<b>┃</b>\n"
        "<b>┃ 🛠 sʏsᴛᴇᴍ ᴄᴏɴᴛʀᴏʟ:</b>\n"
        "<b>┃</b> <i>ᴋᴇᴇᴘ ʏᴏᴜʀ ʙᴏᴛ ᴜᴘ-ᴛᴏ-ᴅᴀᴛᴇ ᴀʟᴡᴀʏs.</i>\n"
        "<b>┃</b> ➔ <code>.update deploy</code>\n"
        "<b>┃</b>\n"
        "<b>┣━━━〔 ᴏꜰꜰɪᴄɪᴀʟ ʟɪɴᴋꜱ 〕━━━┈⊷</b>\n"
        "<b>┃</b>\n"
        "<b>┃ ‣ ᴅᴇᴠᴇʟᴏᴘᴇʀ:</b> @room_cut\n"
        "<b>┃ ‣ ᴜᴘᴅᴀᴛᴇꜱ:</b> @faithxxxx\n"
        "<b>┃ ‣ sᴜᴘᴘᴏʀᴛ:</b> @nobmz\n"
        "<b>┃</b>\n"
        "<b>╰━━━━━━━〔 ɴᴏʙɪᴛᴀ 〕━━━━━━┈⊷</b>"
    )

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
            InlineKeyboardButton("📂 sᴏᴜʀᴄᴇ", url="t.me/Ogdoremonn"),
        ]
    ]

    await message.reply_photo(
        photo=ALIVE_PIC,
        caption=START_TEXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

# Callback Handler for Approval
@app.on_callback_query(filters.regex(r"approve_(\d+)"))
async def approve_callback(client: app, cb: CallbackQuery):
    if cb.from_user.id != OWNER_ID:
        return await cb.answer("❌ Only Owner can approve!", show_alert=True)
    
    user_id = int(cb.data.split("_")[1])
    await approved_users.update_one({"user_id": user_id}, {"$set": {"approved": True}}, upsert=True)
    await cb.answer("✅ User Approved!", show_alert=True)
    await cb.message.edit_text(f"✅ ᴜsᴇʀ <code>{user_id}</code> ʜᴀs ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ!")
    try:
        await client.send_message(user_id, "<b>🎉 ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs!</b>\nʏᴏᴜʀ ᴀᴄᴄᴇss ʜᴀs ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ. ᴛʏᴘᴇ /start ᴛᴏ ʙᴇɢɪɴ.")
    except:
        pass
