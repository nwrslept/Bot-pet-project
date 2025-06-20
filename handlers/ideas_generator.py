from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import os
from dotenv import load_dotenv
import google.generativeai as genai
from keyboards.inline.ideas import idea_difficulty_keyboard

router = Router()

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

@router.message(F.text == "💡 Згенерувати ідею")
async def choose_difficulty(message: Message):
    await message.answer(
        "Оберіть складність ідеї:",
        reply_markup=idea_difficulty_keyboard()
    )

@router.callback_query(F.data.startswith("idea:"))
async def generate_idea_by_difficulty(callback: CallbackQuery):
    difficulty = callback.data.split(":")[1]

    prompts = {
        "easy": "Згенеруй просту не повторювану ідею для Python скрипта, яку нескладно зробити, напиши лише короткий опис самого скрипта",
        "medium": "Згенеруй цікаву не повторювану ідею для python скрипта середньої складності, напиши лише короткий опис самого скрипта.",
        "hard": "Згенеруй складну не повторювану ідею Python скрипта яка потребує продвинутих знань, напиши лише короткий опис самого скрипта.",
    }

    prompt = prompts.get(difficulty, prompts["medium"])

    try:
        await callback.message.edit_text("🔄 Генеруємо ідею...")
        await callback.bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")

        response = model.generate_content(prompt)
        await callback.message.edit_text(f"💡 Ідея ({difficulty}):\n{response.text}")
        await callback.answer()
    except Exception as e:
        await callback.message.edit_text(f"⚠ Помилка при генерації ідеї:\n{e}")
