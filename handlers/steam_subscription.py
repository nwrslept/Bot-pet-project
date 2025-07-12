from aiogram import Bot
from database.subscriptions import get_steam_subscribers
from utils.free_games import get_discounted_to_free_games
from lang.messages import t, get_user_language
import asyncio

async def send_steam_free_games_all_users(bot: Bot):
    users = get_steam_subscribers()
    games = await get_discounted_to_free_games()

    for user_id in users:
        lang = get_user_language(user_id)

        if games:
            text = f"<b>🎮 {t(lang, 'steam.daily_free_games')}:</b>\n\n"
            for game in games[:5]:  # Перші 5 ігор
                text += f"• <b>{game['name']}</b>\n🔗 {game['url']}\n\n"
        else:
            text = f"{t(lang, 'steam.no_free_games')}"

        try:
            await bot.send_message(user_id, text, parse_mode="HTML")
            await asyncio.sleep(0.3)
        except Exception as e:
            print(f"❌ Не вдалося надіслати ігри {user_id}: {e}")
