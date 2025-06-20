from database.db import get_connection


#оновлення підписки на новини
def update_frequency(telegram_id: int, frequency: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO subscriptions (user_id, frequency)
    VALUES ((SELECT id FROM users WHERE telegram_id = ?), ?)
    ON CONFLICT(user_id) DO UPDATE SET frequency = excluded.frequency;
    """, (telegram_id, frequency))

    conn.commit()
    conn.close()


#оновлення вибраних ием новин
def update_topics(telegram_id: int, topics: list[str]):
    topics_str = ",".join(topics)
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE subscriptions
    SET topics = ?
    WHERE user_id = (SELECT id FROM users WHERE telegram_id = ?)
    """, (topics_str, telegram_id))

    conn.commit()
    conn.close()


#відписка і дізлайккк
def remove_subscription(telegram_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM subscriptions
    WHERE user_id = (SELECT id FROM users WHERE telegram_id = ?)
    """, (telegram_id,))

    conn.commit()
    conn.close()

#отримуємо список тем користувача
def get_user_topics(telegram_id: int) -> list[str]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT topics FROM subscriptions
    WHERE user_id = (SELECT id FROM users WHERE telegram_id = ?)
    """, (telegram_id,))
    row = cursor.fetchone()
    conn.close()

    if row and row[0]:
        return row[0].split(",")
    return []


#отримуєм список усіх активних підписок користувачів
def get_all_subscriptions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT u.telegram_id, s.topics, s.frequency
    FROM subscriptions s
    JOIN users u ON u.id = s.user_id
    WHERE s.frequency IS NOT NULL AND s.topics IS NOT NULL AND s.topics != ''
    """)
    result = cursor.fetchall()
    conn.close()

    return [
        {"telegram_id": row[0], "topics": row[1], "frequency": row[2]}
        for row in result
    ]

