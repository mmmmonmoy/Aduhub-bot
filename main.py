import asyncio
import random
import time
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import *
from data import users, source_stats

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Adult images (soft)
IMAGES = [
    "https://i.imgur.com/9ZQZ6xF.jpg",
    "https://i.imgur.com/L7QZK5U.jpg",
    "https://i.imgur.com/8QxQZpR.jpg"
]

CAPTIONS = [
    "🔥 ধন্যবাদ! এক্সক্লুসিভ 18+ কনটেন্ট",
    "🔞 Only for adult users",
    "💋 প্রাইভেট কনটেন্ট আনলক করুন"
]


@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    source = message.get_args() or "direct"

    # First time user
    if user_id not in users:
        users[user_id] = {"last_ad": 0, "source": source}
        source_stats[source] = source_stats.get(source, 0) + 1

    now = time.time()

    # Show ads every 24h
    if now - users[user_id]["last_ad"] > AD_INTERVAL:
        users[user_id]["last_ad"] = now

        smart_link = random.choice(MONETAG_LINKS)
        await message.answer(smart_link)

        if RICHADS_LINK:
            await message.answer(RICHADS_LINK)

    # Buttons
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        types.InlineKeyboardButton(
            "🎬 LIVE দেখুন",
            url=LIVE_BUTTON_LINK
        )
    )

    keyboard.add(
        types.InlineKeyboardButton("🔞 গ্রুপ ১", url=GROUP1),
        types.InlineKeyboardButton("🔞 গ্রুপ ২", url=GROUP2)
    )

    caption_text = (
        f"{random.choice(CAPTIONS)}\n\n"
        "🔴 লাইভ দেখতে নিচে ক্লিক করুন ⬇"
    )

    await message.answer_photo(
        photo=random.choice(IMAGES),
        caption=caption_text,
        reply_markup=keyboard
    )


@dp.message(Command("start"))
async def stats(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    text = "📊 Traffic Source Stats:\n\n"
    for src, count in source_stats.items():
        text += f"• {src} → {count} users\n"

    await message.answer(text)


if __name__ == "__main__":

    asyncio.run(main())






