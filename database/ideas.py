import sqlite3
from datetime import datetime

DB_PATH = "bot_database.db"  # або імпортуй з config, якщо маєш

def save_idea(difficulty: str, idea_text: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS generated_ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            difficulty TEXT,
            idea_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        INSERT INTO generated_ideas (difficulty, idea_text)
        VALUES (?, ?)
    """, (difficulty, idea_text))

    # Видаляємо старі ідеї, лишаємо лише останні 20
    cursor.execute("""
        DELETE FROM generated_ideas
        WHERE id NOT IN (
            SELECT id FROM generated_ideas
            ORDER BY timestamp DESC
            LIMIT 20
        )
    """)

    conn.commit()
    conn.close()

def get_ideas_by_difficulty(difficulty: str, limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT idea_text FROM generated_ideas
        WHERE difficulty = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (difficulty, limit))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]
