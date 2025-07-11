import aiohttp
from aiogram import Router, F
from aiogram.types import Message
from database.steam import set_steam_id, get_steam_id
from handlers.steam_api import get_friends, get_player_statuses
from dotenv import load_dotenv
import os
import re

router = Router()

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")


@router.message(F.text.startswith("steam "))
async def add_steam_profile(message: Message):
    steam_input = message.text.strip().split(" ", 1)[1]
    await process_steam_input(message, steam_input)


@router.message(F.text.regexp(r"(https?://)?steamcommunity\.com/(id|profiles)/[^\s]+"))
async def add_steam_profile_by_link(message: Message):
    steam_input = message.text.strip()
    await process_steam_input(message, steam_input)


async def process_steam_input(message: Message, steam_input: str):
    # Якщо це посилання
    if "steamcommunity.com" in steam_input:
        match = re.search(r"/id/([^/]+)|/profiles/(\d+)", steam_input)
        if match:
            custom_id = match.group(1)
            steam_id64 = match.group(2)

            if steam_id64:
                steam_id = steam_id64
            else:
                steam_id = await resolve_vanity(custom_id)
                if not steam_id:
                    await message.answer("Не вдалося знайти профіль за посиланням.")
                    return
        else:
            await message.answer("Невірне посилання на профіль.")
            return
    else:
        steam_id = steam_input.strip()

    set_steam_id(message.from_user.id, steam_id)
    await message.answer("✅ Твій Steam-профіль збережено!")


async def resolve_vanity(vanity_url: str) -> str | None:
    url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
    params = {
        "key": STEAM_API_KEY,
        "vanityurl": vanity_url
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()
            if data["response"]["success"] == 1:
                return data["response"]["steamid"]
            else:
                return None


@router.message(F.text == "🎮 Steam")
async def steam_main_handler(message: Message):
    telegram_id = message.from_user.id
    steam_id = get_steam_id(telegram_id)

    if not steam_id:
        await message.answer(
            "👋 Схоже, ти ще не додав свій Steam-профіль.\n\n"
            "Введи свій SteamID64 або посилання на профіль:\n"
            "🔹 https://steamcommunity.com/id/твій_нік\n"
            "🔹 або https://steamcommunity.com/profiles/цифри\n\n"
            "Приклад: steam https://steamcommunity.com/id/magistro"
        )
        return

    await message.answer("⏳ Шукаю друзів онлайн...")

    friend_ids = await get_friends(steam_id)
    if not friend_ids:
        await message.answer("⚠️ Не вдалося отримати список друзів. Можливо, профіль або список друзів приватні.")
        return

    players = await get_player_statuses(friend_ids[:100])  # максимум 100 ID за запит
    online = [
        f"🟢 {p['personaname']} — 🎮 {p.get('gameextrainfo', 'у мережі')}"
        for p in players if p["personastate"] != 0
    ]

    text = "\n".join(online) if online else "😴 Ніхто з друзів не в мережі"
    await message.answer(text)
