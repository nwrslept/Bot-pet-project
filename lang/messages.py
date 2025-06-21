from database.db import get_connection

MESSAGES = {

"uk": {
        "start1": "👋 Вітаю, {user}!",
        "start2": "Це мій невеличкий пет-проєкт — 🛠️ Telegram-бот-помічник,"
                  " який допоможе зробити твої повсякденні справи простішими та приємнішими 😌",
        "start3": "Вибери дію з меню нижче 👇",

        "menu_profile": "👤 Профіль",
        "profile_title": "👤 Твій профіль:",
        "profile_id": "🆔 Telegram ID: ",
        "profile_username": "👥 Username: ",
        "profile_first_name": "📛 Ім’я: ",
        "button_saved_ideas": "📚 Мої збережені ідеї",
        "profile_not_found": "❌ Тебе немає в базі даних.",
        "no_ideas": "У тебе поки немає збережених ідей.",
        "button_delete": "❌ Видалити",
        "idea_deleted": "Ідею видалено ✅",
        "choosed_language": "Мову змінено",
        "menu_language": "🌍 Мова",
        "menu_chat_gemini": "🤖 Чат з Gemini",
        "menu_generate_idea": "💡 Згенерувати ідею",
        "menu_news": "📰 Новини",
        "button_leave_chat": "🚪 Покинути чат",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",


    },

    "en": {
        "start1": "👋 Hello {user}!",
        "start2": "This is my little pet project — 🛠️ A Telegram bot assistant "
                  "that will help make your everyday tasks easier and more enjoyable 😌",
        "start3": "Choose an action from the menu below 👇",

        "menu_profile": "👤 Profile",
        "profile_title": "👤 Your profile:",
        "profile_id": "🆔 Telegram ID: ",
        "profile_username": "👥 Username: ",
        "profile_first_name": "📛 Name: ",
        "button_saved_ideas": "📚 My saved ideas",
        "profile_not_found": "❌ You are not in the database.",
        "no_ideas": "You don't have any saved ideas yet.",
        "button_delete": "❌ Delete",
        "idea_deleted": "Idea deleted ✅",
        "choosed_language": "Language changed",
        "menu_language": "🌍 Language",
        "menu_chat_gemini": "🤖 Chat with Gemini",
        "menu_generate_idea": "💡 Generate idea",
        "menu_news": "📰 News",
        "button_leave_chat": "🚪 Leave chat",


    },

}

def t(lang: str, key: str, **kwargs) -> str:
    """Отримати повідомлення за ключем і мовою, з підстановкою значень."""
    text = MESSAGES.get(lang, MESSAGES["en"]).get(key, key)
    return text.format(**kwargs)

def get_user_language(telegram_id: int) -> str:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT language FROM users WHERE telegram_id = ?", (telegram_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "uk"  # fallback

