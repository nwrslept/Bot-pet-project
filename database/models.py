from database.db import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Таблиця користувачів
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        username TEXT,
        first_name TEXT,
        last_name TEXT
    );
    """)

    # Таблиця підписок
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        user_id INTEGER PRIMARY KEY,
        frequency INTEGER DEFAULT 1,
        topics TEXT DEFAULT '',
        is_active INTEGER DEFAULT 1,
        FOREIGN KEY(user_id) REFERENCES users(telegram_id)
    );
    """)

    # Таблиця для чат-історії Gemini
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_message TEXT,
        bot_response TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(telegram_id)
    );
    """)

    # ✅ Таблиця для збережених ідей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS generated_ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            difficulty TEXT,
            idea_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # ✅ Один раз коміт і закриття
    conn.commit()
    conn.close()
