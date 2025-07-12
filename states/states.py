from aiogram.fsm.state import StatesGroup, State

class IdeaGeneration(StatesGroup):
    choosing_topic = State()
    choosing_difficulty = State()

class SteamStates(StatesGroup):
    waiting_for_new_steam_id = State()
