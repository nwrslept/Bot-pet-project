from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.reply import main_menu_keyboard

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

#ініціалізація моделі
model = genai.GenerativeModel("gemini-1.5-flash-latest")

router = Router()

# Стан чату
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
        response = model.generate_content(user_input)
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"⚠ Помилка при зверненні до Gemini:\n{e}")
