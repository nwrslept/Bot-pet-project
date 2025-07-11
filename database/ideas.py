import sqlite3

DB_PATH = "bot_database.db"

def save_idea(topic: str, difficulty: str, idea_text: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS generated_ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            difficulty TEXT,
            idea_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        INSERT INTO generated_ideas (topic, difficulty, idea_text)
        VALUES (?, ?, ?)
    """, (topic, difficulty, idea_text))

    cursor.execute("""
        DELETE FROM generated_ideas
        WHERE id NOT IN (
            SELECT id FROM generated_ideas
            WHERE topic = ? AND difficulty = ?
            ORDER BY timestamp DESC
            LIMIT 20
        ) AND topic = ? AND difficulty = ?
    """, (topic, difficulty, topic, difficulty))

    conn.commit()
    conn.close()


def get_ideas_by_topic_and_difficulty(topic: str, difficulty: str, limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT idea_text FROM generated_ideas
        WHERE topic = ? AND difficulty = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (topic, difficulty, limit))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def save_user_idea(telegram_id: int, topic: str, difficulty: str, idea_text: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_saved_ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            idea_text TEXT,
            topic TEXT,
            difficulty TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        INSERT INTO user_saved_ideas (telegram_id, topic, difficulty, idea_text)
        VALUES (?, ?, ?, ?)
    """, (telegram_id, topic, difficulty, idea_text))

    conn.commit()
    conn.close()

def get_user_ideas(telegram_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, topic, difficulty, idea_text FROM user_saved_ideas
        WHERE telegram_id = ?
        ORDER BY timestamp DESC
    """, (telegram_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_user_idea(idea_id: int, telegram_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM user_saved_ideas
        WHERE id = ? AND telegram_id = ?
    """, (idea_id, telegram_id))
    conn.commit()
    conn.close()


