import os
import asyncio
import time
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from Zaid import app, API_ID, API_HASH
from config import OWNER_ID, ALIVE_PIC, MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient

# --- MongoDB Setup ---
db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client.Nobita_Bot
approved_users = db.approved_users

# Approval Check Function
async def is_approved(user_id):
    if user_id == int(OWNER_ID):
        return True
    user = await approved_users.find_one({"user_id": user_id})
    return bool(user)

# --- START MESSAGE DESIGN ---
START_TEXT = (
    "<b>╭━━━〔 ɴᴏʙɪᴛᴀ ᴜꜱᴇʀʙᴏᴛ ᴠɪᴘ 〕━━━┈⊷</b>\n"
    "<b>┃</b>\n"
    "<b>┃ 👤 ᴡᴇʟᴄᴏᴍᴇ:</b> <a href='tg://user?id={user_id}'>{first_name}</a>\n"
    "<b>┃ 🤖 sᴛᴀᴛᴜs:</b> <code>ᴀᴘᴘʀᴏᴠᴇᴅ ✅</code>\n"
    "<b>┃ ⚙️ ᴇɴɢɪɴᴇ:</b> <code>ɴᴏʙɪ-ᴠ2.5</code>\n"
    "<b>┃</b>\n"
    "<b>┣━━━〔 ᴄʟᴏɴᴇ ꜱʏꜱᴛᴇᴍ 〕━━━┈⊷</b>\n"
    "<b>┃</b>\n"
    "<b>┃</b> <i>ᴀᴘɴᴇ ᴅᴏᴏꜱʀᴇ ᴄʟɪᴇɴᴛꜱ ᴋᴏ ʜᴏꜱᴛ ᴋᴀʀɴᴇ ᴋᴇ ʟɪʏᴇ</i>\n"
    "<b>┃</b> ➔ <code>/clone [ᴘʏʀᴏɢʀᴀᴍ_ꜱᴇꜱꜱɪᴏɴ]</code>\n"
    "<b>┃</b>\n"
    "<b>┣━━━〔 sʏsᴛᴇᴍ ᴄᴏɴᴛʀᴏʟ 〕━━━┈⊷</b>\n"
    "<b>┃</b>\n"
    "<b>┃ ‣ ᴜᴘᴅᴀᴛᴇ:</b> <code>.update deploy</code>\n"
    "<b>┃ ‣ ʀᴇsᴛᴀʀᴛ:</b> <code>.restart</code>\n"
    "<b>┃</b>\n"
    "<b>┣━━━〔 ᴏꜰꜰɪᴄɪᴀʟ ʟɪɴᴋꜱ 〕━━━┈⊷</b>\n"
    "<b>┃</b>\n"
    "<b>┃ ‣ ᴅᴇᴠᴇʟᴏᴘᴇʀ:</b> @room_cut\n"
    "<b>┃ ‣ ᴜᴘᴅᴀᴛᴇꜱ:</b> @faithxxxx\n"
    "<b>┃</b>\n"
    "<b>╰━━━━━━━〔 ɴᴏʙɪᴛᴀ 〕━━━━━━┈⊷</b>"
)

# --- START HANDLER ---
@app.on_message(filters.command("start"))
async def start_handler(client: app, message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    if not await is_approved(user_id):
        await client.send_message(
            int(OWNER_ID),
            f"<b>🔔 ɴᴇᴡ ᴀᴄᴄᴇss ʀᴇǫᴜᴇsᴛ!</b>\n\n<b>👤 ᴜsᴇʀ:</b> {first_name}\n<b>🆔 ɪᴅ:</b> <code>{user_id}</code>",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(f"✅ Approve {first_name}", callback_data=f"approve_{user_id}")
            ]])
        )
        return await message.reply_photo(
            photo=ALIVE_PIC,
            caption=(
                f"<b>❌ Access Denied!</b>\n\nHey {first_name}, aap approved nahi hain.\n"
                "Pehle admin @room_cut se approval lein."
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("📩 Request Approval", url="https://t.me/room_cut")
            ]])
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
        [InlineKeyboardButton("👤 ᴏᴡɴᴇʀ", url="https://t.me/room_cut")]
    ]
    
    await message.reply_photo(
        photo=ALIVE_PIC,
        caption=START_TEXT.format(user_id=user_id, first_name=first_name),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

# --- MANUAL APPROVE COMMAND (/approve user_id) ---
@app.on_message(filters.user(OWNER_ID) & filters.command("approve"))
async def manual_approve(client: app, message: Message):
    if len(message.command) < 2:
        return await message.reply("<b>❌ Usage:</b> <code>/approve [user_id]</code>")
    
    try:
        user_id = int(message.command[1])
        await approved_users.update_one({"user_id": user_id}, {"$set": {"approved": True}}, upsert=True)
        await message.reply(f"<b>✅ User <code>{user_id}</code> ko approve kar diya gaya hai!</b>")
        try:
            await client.send_message(user_id, "<b>🎉 Congratulations!</b>\nAdmin ne aapko manually approve kar diya hai. /start karke bot use karein.")
        except:
            pass
    except ValueError:
        await message.reply("<b>❌ Error:</b> Invalid User ID.")

# --- CALLBACK APPROVE HANDLER ---
@app.on_callback_query(filters.regex(r"approve_(\d+)"))
async def approve_callback(client: app, cb: CallbackQuery):
    if cb.from_user.id != int(OWNER_ID):
        return await cb.answer("❌ Only Owner can do this!", show_alert=True)
    
    user_id = int(cb.data.split("_")[1])
    await approved_users.update_one({"user_id": user_id}, {"$set": {"approved": True}}, upsert=True)
    
    await cb.answer("User Approved Successfully! ✅", show_alert=True)
    await cb.edit_message_caption(caption=f"✅ User <code>{user_id}</code> approved.")
    
    try:
        await client.send_message(user_id, "<b>🎉 Congratulations!</b>\nAdmin ne aapka access approve kar diya hai.")
    except:
        pass

# --- CLONE HANDLER ---
@app.on_message(filters.command("clone"))
async def clone_handler(bot: app, msg: Message):
    if not await is_approved(msg.from_user.id):
        return await msg.reply("❌ Pehle approval lein!")
    
    if len(msg.command) < 2:
        return await msg.reply("<b>Usage:</b> <code>/clone [string_session]</code>")

    session = msg.command[1]
    status = await msg.reply("<code>⌛ Booting Your Client...</code>")
    
    try:
        new_client = Client(
            name=f"Nobita_{msg.from_user.id}_{int(time.time())}", 
            api_id=API_ID, 
            api_hash=API_HASH, 
            session_string=session, 
            plugins=dict(root="Zaid/modules")
        )
        await new_client.start()
        user = await new_client.get_me()
        await status.edit(f"<b>✅ Successfully Started as {user.first_name}!</b>")
    except Exception as e:
        await status.edit(f"<b>❌ ERROR:</b>\n<code>{str(e)}</code>")
        
