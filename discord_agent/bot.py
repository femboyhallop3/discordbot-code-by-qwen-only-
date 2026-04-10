"""
Основной модуль Discord бота
"""
import discord
from discord.ext import commands
import os
import sys

# Импортируем модули
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DISCORD_BOT_TOKEN, OPENROUTER_API_KEY, MODEL_NAME, MAX_MEMORY_SIZE
from memory import memory_manager
from openrouter_client import OpenRouterClient

# Настройка логирования
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем интенты для бота
intents = discord.Intents.default()
intents.message_content = True  # Включаем чтение содержимого сообщений
intents.members = True  # Включаем доступ к информации о пользователях

# Создаем бота
bot = commands.Bot(command_prefix='!', intents=intents)

# Инициализация клиента OpenRouter
openrouter_client = OpenRouterClient(OPENROUTER_API_KEY, MODEL_NAME)

@bot.event
async def on_ready():
    """Событие при запуске бота"""
    logger.info(f'Бот {bot.user} успешно запущен!')
    logger.info(f'ID: {bot.user.id}')
    logger.info('--------')
    
    # Синхронизация слэш-команд
    await bot.tree.sync()
    print("Слэш-команды синхронизированы")

@bot.event
async def on_message(message):
    """Обработка входящих сообщений"""
    # Игнорируем сообщения от самого бота
    if message.author == bot.user:
        return
    
    # Проверяем, упомянут ли бот
    if bot.user in message.mentions:
        await handle_mention(message)
    
    # Продолжаем обработку команд
    await bot.process_commands(message)

async def handle_mention(message: discord.Message):
    """Обработка упоминания бота"""
    logger.info(f'Получено упоминание от {message.author.name}: {message.content}')
    
    # Извлекаем текст сообщения без упоминания
    content = message.content.replace(f'<@{bot.user.id}>', '').strip()
    
    if not content:
        await message.channel.send("Да, я здесь! Чем могу помочь?")
        return
    
    # Получаем историю для этого пользователя
    user_id = str(message.author.id)
    history = memory_manager.get_history(user_id)
    
    # Формируем полный запрос
    full_messages = [
        {
            "role": "system",
            "content": "Ты дружелюбный AI агент в Discord. Твое имя - DeepBot. Отвечай кратко, но информативно."
        }
    ]
    
    # Добавляем историю из памяти
    for msg in history:
        full_messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    # Добавляем новое сообщение пользователя
    full_messages.append({
        "role": "user",
        "content": content
    })
    
    # Показываем статус "печатает..."
    async with message.channel.typing():
        # Получаем ответ от AI
        response = openrouter_client.generate_response(full_messages, user_id)
    
    if response:
        # Добавляем сообщения в память
        memory_manager.add_message(user_id, "user", content)
        memory_manager.add_message(user_id, "assistant", response)
        
        # Сохраняем память
        memory_manager.save_memory()
        
        # Отправляем ответ
        await message.reply(response)
        logger.info(f'Отправлен ответ пользователю {message.author.name}')
    else:
        await message.channel.send("Извините, я столкнулся с проблемой при генерации ответа. Попробуйте позже.")
        logger.error(f'Не удалось получить ответ для пользователя {message.author.name}')

# Команда для очистки памяти
@bot.command(name='clear')
async def clear_memory(ctx):
    """Очищает память бота для пользователя"""
    user_id = str(ctx.author.id)
    memory_manager.clear_memory(user_id)
    memory_manager.save_memory()
    await ctx.send(f"Память для {ctx.author.mention} очищена!")

# Команда для информации о памяти
@bot.command(name='memory')
async def show_memory(ctx):
    """Показывает количество сообщений в памяти"""
    user_id = str(ctx.author.id)
    count = len(memory_manager.get_history(user_id))
    await ctx.send(f"В памяти {count} сообщений из {MAX_MEMORY_SIZE} возможных.")

# Команда для перезагрузки модулей (для разработки)
@bot.command(name='reload')
async def reload_modules(ctx):
    """Перезагружает модули (только для разработчиков)"""
    if ctx.author.id == int(os.environ.get('DEVELOPER_ID', '0')):
        try:
            # Перезагрузка модулей (упрощенная версия)
            import importlib
            import memory
            import openrouter_client
            importlib.reload(memory)
            importlib.reload(openrouter_client)
            await ctx.send("Модули перезагружены!")
        except Exception as e:
            await ctx.send(f"Ошибка перезагрузки: {e}")
    else:
        await ctx.send("У вас нет прав для выполнения этой команды!")

# Запуск бота
def main():
    """Главная функция запуска"""
    if not DISCORD_BOT_TOKEN or not OPENROUTER_API_KEY:
        print("Ошибка: Проверьте файл config.py - укажите токены!")
        return
    
    logger.info("Запуск Discord AI Агента...")
    bot.run(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    main()
