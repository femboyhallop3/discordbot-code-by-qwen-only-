# Конфигурация бота
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем токены из переменных окружения или используем значения по умолчанию
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN', 'your_discord_bot_token_here')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', 'your_openrouter_api_key_here')

# Настройки модели
MODEL_NAME = "deepseek/deepseek-v3.2"
MAX_MEMORY_SIZE = 20  # Увеличили размер памяти для канала

# Настройки промптов
DEFAULT_PROMPT_TYPE = "memory"  # Использовать промпт с памятью по умолчанию

# Настройки обнаружения важных сообщений
IMPORTANT_MESSAGE_INDICATORS = [
    "важно", "срочно", "внимание", "приоритет",
    "решение", "итог", "вывод", "результат"
]
