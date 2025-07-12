from database.db import get_connection


# Оновлення підписки на частоту новин
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


# Оновлення вибраних тем новин
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


# Відписка (видалення підписки) повністю
def remove_subscription(telegram_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM subscriptions
    WHERE user_id = (SELECT id FROM users WHERE telegram_id = ?)
    """, (telegram_id,))

    conn.commit()
    conn.close()


# Отримуємо список тем користувача
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


# Оновлення/додавання підписки на роздачі Steam (булеве поле)
def update_steam_subscription(telegram_id: int, subscribed: bool):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO subscriptions (user_id, is_steam_subscribed)
    VALUES ((SELECT id FROM users WHERE telegram_id = ?), ?)
    ON CONFLICT(user_id) DO UPDATE SET is_steam_subscribed = excluded.is_steam_subscribed;
    """, (telegram_id, int(subscribed)))

    conn.commit()
    conn.close()


# Перевірка, чи користувач підписаний на роздачі Steam
def is_user_steam_subscribed(telegram_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT is_steam_subscribed FROM subscriptions
    WHERE user_id = (SELECT id FROM users WHERE telegram_id = ?)
    """, (telegram_id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return bool(row[0])
    return False


# Отримати список усіх підписаних на роздачі Steam
def get_steam_subscribers() -> list[int]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT u.telegram_id FROM subscriptions s
    JOIN users u ON s.user_id = u.id
    WHERE s.is_steam_subscribed = 1
    """)

    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows]


# Отримуємо список усіх активних підписок користувачів (з темами, частотою, і тепер is_steam_subscribed)
def get_all_subscriptions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT u.telegram_id, s.topics, s.frequency, s.is_steam_subscribed
    FROM subscriptions s
    JOIN users u ON u.id = s.user_id
    WHERE s.frequency IS NOT NULL AND s.topics IS NOT NULL AND s.topics != ''
    """)
    result = cursor.fetchall()
    conn.close()

    return [
        {
            "telegram_id": row[0],
            "topics": row[1],
            "frequency": row[2],
            "is_steam_subscribed": bool(row[3]) if row[3] is not None else False
        }
        for row in result
    ]
