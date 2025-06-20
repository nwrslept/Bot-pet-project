from handlers.news_api import get_news
import asyncio

async def send_news_to_user(bot, telegram_id: int, topics: list[str]):
    if not topics:
        return

    for topic in topics:
        articles, error = get_news(category=topic, page=1)
        if error or not articles:
            continue

        article = articles[0]
        text = f"<b>{article['title']}</b>\n{article['url']}"

        try:
            await bot.send_message(chat_id=telegram_id, text=text, parse_mode="HTML")
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Error sending news to {telegram_id}: {e}")

async def send_news_all_users(bot, frequency_times_per_day: int, get_all_subscriptions):
    users = get_all_subscriptions()
    for user in users:
        if user['frequency'] == frequency_times_per_day:
            topics = user['topics'].split(",") if user['topics'] else []
            await send_news_to_user(bot, user['telegram_id'], topics)
