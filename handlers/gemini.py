from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.reply import main_menu_keyboard, gemini_left_chat
import os
from dotenv import load_dotenv
import google.generativeai as genai
from database.gemini_history import save_message, get_last_messages
from lang.messages import t, get_user_language


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

router = Router()

class ChatStates(StatesGroup):
    chatting = State()

@router.message(F.text.in_({"🤖 Чат з Gemini", "🤖 Chat with Gemini"}) )
async def start_chat(message: Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    await state.set_state(ChatStates.chatting)
    await message.answer(t(lang, "chat_start"), reply_markup=gemini_left_chat(lang))

@router.message(F.text.in_({"🚪 Покинути чат", "🚪 Leave chat"}))
async def left_chat(message: Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    await state.clear()
    await message.answer(t(lang, "chat_exit"), reply_markup=main_menu_keyboard(lang))

@router.message(ChatStates.chatting)
async def chat_with_gemini(message: Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    user_input = message.text
    try:
        await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

        history = get_last_messages(message.from_user.id)

        context_text = t(lang, "chat_context_instruction") + "\n"
        for user_msg, bot_resp in history:
            context_text += f"User: {user_msg}\nBot: {bot_resp}\n"
        context_text += f"User: {user_input}\nBot:"

        response = model.generate_content(context_text)

        save_message(message.from_user.id, user_input, response.text)

        await message.answer(response.text)
    except Exception as e:
        await message.answer(t(lang, "chat_error", error=str(e)))
