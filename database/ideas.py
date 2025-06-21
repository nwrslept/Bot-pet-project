import sqlite3
from datetime import datetime

DB_PATH = "bot_database.db"  # або імпортуй з config, якщо маєш

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

    # Залишаємо тільки останні 20 ідей для кожної теми + складності
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

