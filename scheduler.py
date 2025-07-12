import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.subscriptions import get_all_subscriptions
from handlers.news_sender import send_news_all_users
from handlers.steam_subscription import send_steam_free_games_all_users

scheduler = AsyncIOScheduler()

def schedule_jobs(bot):
    loop = asyncio.get_event_loop()

    def job_wrapper(frequency):
        #запуск корутини у поточному лупі thread-safe способом
        asyncio.run_coroutine_threadsafe(send_news_all_users(bot, frequency, get_all_subscriptions), loop)

    scheduler.add_job(lambda: job_wrapper(1), 'cron', hour=12, minute=0, id="news_1")
    scheduler.add_job(lambda: job_wrapper(2), 'cron', hour=9, minute=0, id="news_2_morning")
    scheduler.add_job(lambda: job_wrapper(2), 'cron', hour=21, minute=0, id="news_2_evening")
    scheduler.add_job(lambda: job_wrapper(3), 'cron', hour=9, minute=0, id="news_3_morning")
    scheduler.add_job(lambda: job_wrapper(3), 'cron', hour=14, minute=0, id="news_3_afternoon")
    scheduler.add_job(lambda: job_wrapper(3), 'cron', hour=21, minute=0, id="news_3_evening")

    # 💥 Нове: Steam free games щодня о 08:00
    scheduler.add_job(lambda: asyncio.run_coroutine_threadsafe(
        send_steam_free_games_all_users(bot), loop),
                      'cron', hour=10, minute=00, id="steam_free_games_daily")

    scheduler.start()
