import sqlite3

# задати steamID
def set_steam_id(telegram_id: int, steam_id: str):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (telegram_id, steam_id)
        VALUES (?, ?)
        ON CONFLICT(telegram_id) DO UPDATE SET steam_id=excluded.steam_id;
    """, (telegram_id, steam_id))
    conn.commit()
    conn.close()

# отримати Steam ID
def get_steam_id(telegram_id: int) -> str | None:
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT steam_id FROM users WHERE telegram_id = ?", (telegram_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None