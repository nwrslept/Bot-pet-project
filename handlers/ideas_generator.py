from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import os
from dotenv import load_dotenv
import google.generativeai as genai
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.inline.ideas import idea_topic_keyboard, idea_difficulty_keyboard
from database.ideas import save_user_idea, get_ideas_by_topic_and_difficulty, save_idea

router = Router()

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# Визначаємо стани
class IdeaGeneration(StatesGroup):
    choosing_topic = State()
    choosing_difficulty = State()

# Старт — вибір теми
@router.message(F.text == "💡 Згенерувати ідею")
async def choose_topic(message: Message, state: FSMContext):
    await state.set_state(IdeaGeneration.choosing_topic)
    await message.answer(
        "Оберіть тему скрипта:",
        reply_markup=idea_topic_keyboard()
    )

# Вибір складності після вибору теми
@router.callback_query(F.data.startswith("topic:"), IdeaGeneration.choosing_topic)
async def choose_difficulty(callback: CallbackQuery, state: FSMContext):
    topic = callback.data.split(":")[1]

    # Зберігаємо тему у FSM
    await state.update_data(topic=topic)

    # Встановлюємо стан вибору складності
    await state.set_state(IdeaGeneration.choosing_difficulty)

    await callback.message.edit_text(
        "Оберіть складність ідеї:",
        reply_markup=idea_difficulty_keyboard(topic)
    )
    await callback.answer()

# Генерація ідеї
@router.callback_query(F.data.startswith("idea:"), IdeaGeneration.choosing_difficulty)
async def generate_idea(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split(":")
    if len(parts) != 3:
        await callback.message.edit_text("⚠ Некоректні дані.")
        return

    _, topic_from_callback, difficulty = parts

    data = await state.get_data()
    topic = data.get("topic") or topic_from_callback

    previous_ideas = get_ideas_by_topic_and_difficulty(topic, difficulty)
    context = "\n".join(f"- {idea}" for idea in previous_ideas)

    prompt = f"""
Ти — генератор ідей для Python-скриптів. Тема: {topic}. Складність: {difficulty}.
Не повторюй попередні ідеї:

{context if context else '(Ще немає попередніх ідей)'}

Згенеруй унікальну коротку ідею скрипта без пояснень та коду.
"""

    try:
        await callback.message.edit_text("🔄 Генеруємо ідею...")
        await callback.bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")

        response = model.generate_content(prompt)
        idea = response.text.strip()

        save_idea(topic, difficulty, idea)  # Зберігаємо в загальну БД

        await state.update_data(generated_idea=idea, generated_topic=topic, generated_difficulty=difficulty)

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="💾 Зберегти ідею", callback_data="save_idea"),
                InlineKeyboardButton(text="🔄 Ще", callback_data="more_idea")
            ]
        ])

        await callback.message.edit_text(
            f"💡 Ідея ({topic}, {difficulty}):\n{idea}",
            reply_markup=keyboard
        )
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text(f"⚠ Помилка при генерації ідеї:\n{e}")

@router.callback_query(F.data == "save_idea")
async def save_idea_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    idea = data.get("generated_idea")
    topic = data.get("generated_topic")
    difficulty = data.get("generated_difficulty")
    telegram_id = callback.from_user.id  # Ось тут отримуємо ID користувача

    if not idea or not topic or not difficulty:
        await callback.answer("Немає ідеї для збереження.", show_alert=True)
        return

    try:
        # Зберігаємо саме у таблицю користувача
        save_user_idea(telegram_id, topic, difficulty, idea)
        await callback.answer("Ідею збережено ✅", show_alert=True)
        await callback.message.edit_reply_markup(None)
        await state.update_data(generated_idea=None, generated_topic=None, generated_difficulty=None)
    except Exception as e:
        await callback.answer(f"Помилка при збереженні: {e}", show_alert=True)

@router.callback_query(F.data == "more_idea")
async def more_idea_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    topic = data.get("generated_topic")
    difficulty = data.get("generated_difficulty")

    if not topic or not difficulty:
        await callback.answer("Немає даних для генерації нової ідеї.", show_alert=True)
        return

    # Викликаємо функцію генерації, але без FSM станів, тому просто повторюємо код генерації
    previous_ideas = get_ideas_by_topic_and_difficulty(topic, difficulty)
    context = "\n".join(f"- {idea}" for idea in previous_ideas)

    prompt = f"""
Ти — генератор ідей для Python-скриптів. Тема: {topic}. Складність: {difficulty}.
Не повторюй попередні ідеї:

{context if context else '(Ще немає попередніх ідей)'}

Згенеруй унікальну коротку ідею скрипта без пояснень та коду.
"""

    try:
        await callback.message.edit_text("🔄 Генеруємо ідею...")
        await callback.bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")

        response = model.generate_content(prompt)
        idea = response.text.strip()

        save_idea(topic, difficulty, idea)

        await state.update_data(generated_idea=idea)

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="💾 Зберегти ідею", callback_data="save_idea"),
                InlineKeyboardButton(text="🔄 Ще", callback_data="more_idea")
            ]
        ])

        await callback.message.edit_text(
            f"💡 Ідея ({topic}, {difficulty}):\n{idea}",
            reply_markup=keyboard
        )
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text(f"⚠ Помилка при генерації ідеї:\n{e}")



