import sqlite3

DB_PATH = "bot_database.db"


def save_message(user_id: int, user_msg: str, bot_resp: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_message TEXT,
            bot_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        INSERT INTO chat_history (user_id, user_message, bot_response)
        VALUES (?, ?, ?)
    """, (user_id, user_msg, bot_resp))
    conn.commit()

    # Видалити старі повідомлення, лишити 10 останніх
    cursor.execute("""
        DELETE FROM chat_history
        WHERE id NOT IN (
            SELECT id FROM chat_history
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT 10
        ) AND user_id = ?
    """, (user_id, user_id))
    conn.commit()
    conn.close()


def get_last_messages(user_id: int, limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_message, bot_response FROM chat_history
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return rows[::-1]  # щоб порядок був від найстарішого до найновішого
