from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from lang.messages import t, get_user_language
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


@router.message(F.text.in_({"🎮 Steam", "🎮 Стім"}))
async def steam_main_handler(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    lang = get_user_language(telegram_id)
    steam_id = get_steam_id(telegram_id)

    if not steam_id:
        await message.answer(t(lang, "steam.add_instruction"))
        await state.set_state(SteamStates.waiting_for_new_steam_id)
        return

    await message.answer(t(lang, "steam.choose_action"), reply_markup=steam_menu_keyboard(lang))


@router.callback_query(F.data == "steam_profile")
async def show_profile(call: CallbackQuery):
    lang = get_user_language(call.from_user.id)
    steam_id = get_steam_id(call.from_user.id)

    if not steam_id:
        await call.message.answer(t(lang, "steam.profile_not_found"))
        return

    profile = await get_player_summary(steam_id)
    if not profile:
        await call.message.answer(t(lang, "steam.profile_error"))
        return

    name = profile["personaname"]
    avatar = profile["avatarfull"]
    profile_url = profile["profileurl"]
    status = profile.get("gameextrainfo", t(lang, "steam.status.offline") if profile["personastate"] == 0 else t(lang, "steam.status.online"))

    text = (
        f"👤 <b>{name}</b>\n"
        f"🔗 <a href='{profile_url}'>{t(lang, 'steam.view_profile')}</a>\n"
        f"🎮 <b>{t(lang, 'steam.status')}:</b> {status}"
    )

    await call.message.delete()
    await call.message.answer_photo(photo=avatar, caption=text, parse_mode="HTML", reply_markup=back_to_steam_menu(lang))
    await call.answer()


@router.callback_query(F.data == "steam_change")
async def change_steam_profile(call: CallbackQuery, state: FSMContext):
    lang = get_user_language(call.from_user.id)
    await call.message.delete()
    await call.message.answer(t(lang, "steam.enter_new"), reply_markup=back_to_steam_menu(lang))
    await state.set_state(SteamStates.waiting_for_new_steam_id)
    await call.answer()


@router.message(SteamStates.waiting_for_new_steam_id)
async def update_steam_profile(message: Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    steam_input = message.text.strip()
    steam_id = await resolve_steam_input(steam_input)

    if not steam_id:
        await message.answer(t(lang, "steam.invalid_input"), reply_markup=back_to_steam_menu(lang))
        return

    set_steam_id(message.from_user.id, steam_id)
    await message.answer(t(lang, "steam.saved"), reply_markup=steam_menu_keyboard(lang))
    await state.clear()


@router.callback_query(F.data == "steam_friends")
async def show_friends(call: CallbackQuery):
    lang = get_user_language(call.from_user.id)
    steam_id = get_steam_id(call.from_user.id)

    if not steam_id:
        await call.message.answer(t(lang, "steam.profile_not_found"), reply_markup=back_to_steam_menu(lang))
        await call.answer()
        return

    await call.message.delete()
    await call.message.answer(t(lang, "steam.finding_friends"))
    await call.answer()

    friend_ids = await get_friends(steam_id)
    if not friend_ids:
        await call.message.answer(t(lang, "steam.no_friends"), reply_markup=back_to_steam_menu(lang))
        return

    players = await get_player_statuses(friend_ids[:100])
    online = [
        f"🟢 {p['personaname']} — 🎮 {p.get('gameextrainfo', t(lang, 'steam.status.online'))}"
        for p in players if p["personastate"] != 0
    ]

    text = "\n".join(online) if online else t(lang, "steam.no_one_online")
    await call.message.answer(t(lang, "steam.friends_online") + "\n\n" + text, reply_markup=back_to_steam_menu(lang))


@router.callback_query(F.data == "steam_back")
async def back_to_menu(call: CallbackQuery):
    lang = get_user_language(call.from_user.id)
    await call.message.delete()
    await call.message.answer(t(lang, "steam.choose_action"), reply_markup=steam_menu_keyboard(lang))
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
