import os
from dotenv import load_dotenv
import google.generativeai as genai

# Завантажує .env файл
load_dotenv()

# Отримує ключ з .env
api_key = os.getenv("GEMINI_API_KEY")

# Налаштовуємо SDK
genai.configure(api_key=api_key)

# Отримуємо список моделей
try:
    models = genai.list_models()
    print("✅ Доступні моделі:")
    for model in models:
        print(f"• {model.name} — підтримує: {model.supported_generation_methods}")
except Exception as e:
    print("⚠ Помилка при спробі отримати список моделей:")
    print(e)
