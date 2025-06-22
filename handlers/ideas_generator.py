from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import os
from dotenv import load_dotenv
import google.generativeai as genai
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from lang.messages import t, get_user_language
from keyboards.inline.ideas import idea_topic_keyboard, idea_difficulty_keyboard
from database.ideas import save_user_idea, get_ideas_by_topic_and_difficulty, save_idea

router = Router()

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

class IdeaGeneration(StatesGroup):
    choosing_topic = State()
    choosing_difficulty = State()

@router.message(F.text.in_({"💡 Згенерувати ідею", "💡 Generate idea"}))
async def choose_topic(message: Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    await state.set_state(IdeaGeneration.choosing_topic)
    await message.answer(
        t(lang, "idea_choose_topic"),
        reply_markup=idea_topic_keyboard(lang)
    )

@router.callback_query(F.data.startswith("topic:"), IdeaGeneration.choosing_topic)
async def choose_difficulty(callback: CallbackQuery, state: FSMContext):
    topic = callback.data.split(":")[1]
    await state.update_data(topic=topic)

    await state.set_state(IdeaGeneration.choosing_difficulty)
    lang = get_user_language(callback.from_user.id)
    await callback.message.edit_text(
        t(lang, "choose_difficulty"),
        reply_markup=idea_difficulty_keyboard(topic, lang)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("idea:"), IdeaGeneration.choosing_difficulty)
async def generate_idea(callback: CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    parts = callback.data.split(":")
    if len(parts) != 3:
        await callback.message.edit_text(t(lang, "idea_invalid_data"))
        return

    _, topic_from_callback, difficulty = parts

    data = await state.get_data()
    topic = data.get("topic") or topic_from_callback

    previous_ideas = get_ideas_by_topic_and_difficulty(topic, difficulty)
    context = "\n".join(f"- {idea}" for idea in previous_ideas) or t(lang, "no_previous_ideas")

    prompt = "\n\n".join([
        t(lang, "idea_prompt", topic=topic, difficulty=difficulty, context=context)

    ])

    try:
        await callback.message.edit_text(t(lang, "generating_idea"))
        await callback.bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")

        response = model.generate_content(prompt)
        idea = response.text.strip()

        save_idea(topic, difficulty, idea)

        await state.update_data(generated_idea=idea, generated_topic=topic, generated_difficulty=difficulty)

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "save_idea_btn"), callback_data="save_idea"),
                InlineKeyboardButton(text=t(lang, "more_idea_btn"), callback_data="more_idea")
            ]
        ])

        await callback.message.edit_text(
            t(lang, "idea_result", topic=topic, difficulty=difficulty, idea=idea),
            reply_markup=keyboard
        )
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text(f"{t(lang, 'idea_error')}\n{e}")

@router.callback_query(F.data == "save_idea")
async def save_idea_handler(callback: CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    data = await state.get_data()
    idea = data.get("generated_idea")
    topic = data.get("generated_topic")
    difficulty = data.get("generated_difficulty")
    telegram_id = callback.from_user.id

    if not idea or not topic or not difficulty:
        await callback.answer(t(lang, "no_idea_to_save"), show_alert=True)
        return

    try:
        save_user_idea(telegram_id, topic, difficulty, idea)
        await callback.answer(t(lang, "idea_saved"), show_alert=True)

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "more_idea_btn"), callback_data="more_idea")]
        ])

        await callback.message.edit_reply_markup(reply_markup=keyboard)

        await state.update_data(generated_idea=None)

    except Exception as e:
        await callback.answer(f"{t(lang, 'idea_save_error')} {e}", show_alert=True)

@router.callback_query(F.data == "more_idea")
async def more_idea_handler(callback: CallbackQuery, state: FSMContext):
    lang = get_user_language(callback.from_user.id)
    data = await state.get_data()
    topic = data.get("generated_topic")
    difficulty = data.get("generated_difficulty")

    if not topic or not difficulty:
        await callback.answer(t(lang, "no_data_for_idea"), show_alert=True)
        return

    previous_ideas = get_ideas_by_topic_and_difficulty(topic, difficulty)
    context = "\n".join(f"- {idea}" for idea in previous_ideas) or t(lang, "no_previous_ideas")

    prompt = "\n\n".join([
        t(lang, "idea_prompt", topic=topic, difficulty=difficulty, context=context)
    ])

    try:
        await callback.message.edit_text(t(lang, "generating_idea"))
        await callback.bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")

        response = model.generate_content(prompt)
        idea = response.text.strip()

        save_idea(topic, difficulty, idea)

        await state.update_data(generated_idea=idea)

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "save_idea_btn"), callback_data="save_idea"),
                InlineKeyboardButton(text=t(lang, "more_idea_btn"), callback_data="more_idea")
            ]
        ])

        await callback.message.edit_text(
            t(lang, "idea_result", topic=topic, difficulty=difficulty, idea=idea),
            reply_markup=keyboard
        )
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text(f"{t(lang, 'idea_error')}\n{e}")
