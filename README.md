# Telegram Bot — News, Gemini Chat, Idea Generator, and Steam

This is a Telegram bot that combines several useful features:
- Sends news by topics
- Chat with the Gemini model for generating responses
- Idea generator with various topics and difficulty levels
- Steam integration: free games, subscription to giveaways, friend status
- Support for two languages: Ukrainian and English

---

## Main Features

- 📰 Display news by topics with subscription options
- 💬 Chat based on the Gemini model for communication and text generation
- 💡 Idea generator by topics, saving ideas in the database to avoid duplicates
- 🎮 Steam: search for free games, subscribe to giveaways, view friends and their statuses
- 🌐 Multilingual support: Ukrainian and English with the ability to switch languages

## Technologies

- Python 3.x
- Aiogram 3.20 for the Telegram bot
- SQLite database for storing user data
- Gemini API for text generation
- Steam API for Steam integration
- Asynchronous requests (aiohttp or requests)
- Translation system for multi-language support

## 🔧 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/nwrslwpt/Bot-pet-project.git  
cd repository-name
```

2. **Create and activate a virtual environment:**

```bash
# Linux/macOS
python -m venv .venv
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables in a `.env` file (create this file in the project root):**

```env
BOT_TOKEN=your_bot_token
GEMINI_API_KEY=your_gemini_api_key
STEAM_API_KEY=your_steam_api_key
DB_PATH=./bot.db
```

5. **Run the bot:**

```bash
python main.py
```

## Usage

- /start — start interacting with the bot  
- 🌐 Change language — you can switch between Ukrainian and English  
- 📰 News — select topics and view the latest news  
- 💬 Chat with Gemini — communicate with the Gemini model  
- 💡 Ideas — generate new ideas by topics  
- 🎮 Steam — view free games and subscribe to giveaways

Each section has its own menu and instructions inside the bot.

## Contribution

Ideas, bug fixes, and improvements are welcome! Fork the repo, create a pull request, or open an issue.
