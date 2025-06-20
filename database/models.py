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
        user_id INTEGER PRIMARY KEY,        -- той самий telegram_id
        frequency INTEGER DEFAULT 1,        -- 1, 2 або 3 рази на день
        topics TEXT DEFAULT '',             -- рядок з темами через кому
        is_active INTEGER DEFAULT 1,        -- 1 = активна, 0 = відписаний
        FOREIGN KEY(user_id) REFERENCES users(telegram_id)
    );
    """)

    conn.commit()
    conn.close()
