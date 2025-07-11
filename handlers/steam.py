from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database.steam import set_steam_id, get_steam_id
from handlers.steam_api import get_friends, get_player_statuses, get_player_summary
from keyboards.inline.steam import steam_menu_keyboard, back_to_steam_menu
from states.states import SteamStates
import re
import aiohttp
import os
from dotenv import load_dotenv

router = Router()
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")


@router.message(F.text == "🎮 Steam")
async def steam_main_handler(message: Message):
    telegram_id = message.from_user.id
    steam_id = get_steam_id(telegram_id)

    if not steam_id:
        await message.answer(
            "👋 Схоже, ти ще не додав свій Steam-профіль.\n\n"
            "Введи свій SteamID64 або посилання на профіль:\n"
        )
        return

    await message.answer("Оберіть дію:", reply_markup=steam_menu_keyboard())


@router.callback_query(F.data == "steam_profile")
async def show_profile(call: CallbackQuery):
    steam_id = get_steam_id(call.from_user.id)
    if not steam_id:
        await call.message.answer("Профіль не знайдено, будь ласка, додайте Steam ID.")
        return

    profile = await get_player_summary(steam_id)
    if not profile:
        await call.message.answer("Не вдалося отримати інформацію про профіль.")
        return

    name = profile["personaname"]
    avatar = profile["avatarfull"]
    profile_url = profile["profileurl"]
    status = profile.get("gameextrainfo", "у мережі" if profile["personastate"] else "офлайн")

    text = (
        f"👤 <b>{name}</b>\n"
        f"🔗 <a href='{profile_url}'>Перейти до профілю</a>\n"
        f"🎮 <b>Статус:</b> {status}"
    )

    await call.message.delete()
    await call.message.answer_photo(photo=avatar, caption=text, parse_mode="HTML", reply_markup=back_to_steam_menu())
    await call.answer()


@router.callback_query(F.data == "steam_change")
async def change_steam_profile(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Введіть новий SteamID64 або посилання на свій Steam-профіль.", reply_markup=back_to_steam_menu())
    await state.set_state(SteamStates.waiting_for_new_steam_id)
    await call.answer()


@router.message(SteamStates.waiting_for_new_steam_id)
async def update_steam_profile(message: Message, state: FSMContext):
    steam_input = message.text.strip()
    steam_id = await resolve_steam_input(steam_input)
    if not steam_id:
        await message.answer("🚫 Невірне посилання або ID. Спробуйте ще раз.", reply_markup=back_to_steam_menu())
        return

    set_steam_id(message.from_user.id, steam_id)
    await message.answer("✅ Новий Steam-профіль збережено!", reply_markup=back_to_steam_menu())
    await state.clear()


@router.callback_query(F.data == "steam_friends")
async def show_friends(call: CallbackQuery):
    steam_id = get_steam_id(call.from_user.id)
    if not steam_id:
        await call.message.answer("Профіль не знайдено, будь ласка, додайте Steam ID.", reply_markup=back_to_steam_menu())
        await call.answer()
        return

    await call.message.delete()
    await call.message.answer("⏳ Шукаю друзів онлайн...")
    await call.answer()

    friend_ids = await get_friends(steam_id)
    if not friend_ids:
        await call.message.answer("⚠️ Не вдалося отримати список друзів. Можливо, профіль або список друзів приватні.", reply_markup=back_to_steam_menu())
        await call.answer()
        return

    players = await get_player_statuses(friend_ids[:100])
    online = [
        f"🟢 {p['personaname']} — 🎮 {p.get('gameextrainfo', 'у мережі')}"
        for p in players if p["personastate"] != 0
    ]

    text = "\n".join(online) if online else "😴 Ніхто з друзів не в мережі"
    await call.message.answer("👥 Ось хто зараз онлайн:\n\n" + text, reply_markup=back_to_steam_menu())
    await call.answer()


async def resolve_steam_input(input_str: str) -> str | None:
    if "steamcommunity.com" in input_str:
        match = re.search(r"/id/([^/]+)|/profiles/(\d+)", input_str)
        if match:
            custom_id = match.group(1)
            steam_id64 = match.group(2)
            if steam_id64:
                return steam_id64
            if custom_id:
                return await resolve_vanity(custom_id)
    elif input_str.isdigit() and len(input_str) >= 17:
        return input_str
    return None


async def resolve_vanity(vanity_url: str) -> str | None:
    url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
    params = {"key": STEAM_API_KEY, "vanityurl": vanity_url}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()
            if data["response"]["success"] == 1:
                return data["response"]["steamid"]
            return None

@router.callback_query(F.data == "steam_back")
async def back_to_menu(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Оберіть дію:", reply_markup=steam_menu_keyboard())
    await call.answer()

