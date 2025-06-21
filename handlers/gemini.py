from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.reply import main_menu_keyboard

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Імпортуємо твої функції з gemini_history.py
from database.gemini_history import save_message, get_last_messages

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash-latest")

router = Router()

class ChatStates(StatesGroup):
    chatting = State()

@router.message(F.text == "🤖 Чат з Gemini")
async def start_chat(message: Message, state: FSMContext):
    await state.set_state(ChatStates.chatting)
    await message.answer("🧠 Ти в чаті з Gemini. Напиши питання!\nЩоб вийти — /exit")

@router.message(ChatStates.chatting, F.text == "/exit")
async def exit_chat(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🚪 Ти вийшов з чату з Gemini.", reply_markup=main_menu_keyboard())

@router.message(ChatStates.chatting)
async def chat_with_gemini(message: Message, state: FSMContext):
    user_input = message.text
    try:
        await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

        # Отримуємо історію останніх 10 повідомлень
        history = get_last_messages(message.from_user.id)

        # Формуємо текст з історією для Gemini
        context_text = "Відповідай українською мовою, дружелюбно, і не сильно розгорнуто якщо цього не попросить корисутвач"
        for user_msg, bot_resp in history:
            context_text += f"User: {user_msg}\nBot: {bot_resp}\n"
        context_text += f"User: {user_input}\nBot:"

        response = model.generate_content(context_text)

        # Зберігаємо повідомлення користувача і відповідь Gemini
        save_message(message.from_user.id, user_input, response.text)

        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"⚠ Помилка при зверненні до Gemini:\n{e}")
