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
from prompts import get_prompt, format_prompt

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
    
    # Используем канал как ключ для памяти
    channel_id = str(message.channel.id)
    user_id = str(message.author.id)
    
    # Получаем историю для этого канала
    history = memory_manager.get_history(channel_id)
    
    # Получаем информацию о канале
    summary = memory_manager.get_chat_summary(channel_id)
    channel_info = {
        "channel_name": message.channel.name if hasattr(message.channel, 'name') else "Direct Message",
        "user_count": len(message.channel.members) if hasattr(message.channel, 'members') else 1,
        "topics": ", ".join(summary.get("topics", [])) if summary else ""
    }
    
    # Получаем важные сообщения и задачи
    important_messages = memory_manager.get_important_messages(channel_id)
    action_items = memory_manager.get_action_items(channel_id)
    
    # Используем улучшенный промпт с памятью
    system_prompt = get_prompt("memory")
    formatted_prompt = format_prompt(system_prompt, 
                                     channel_name=channel_info["channel_name"],
                                     user_count=channel_info["user_count"],
                                     topics=channel_info["topics"],
                                     chat_history=str(history[-3:] if len(history) > 3 else history),
                                     important_messages=str(important_messages[-2:] if len(important_messages) > 2 else important_messages),
                                     action_items=str(action_items))
    
    # Формируем полный запрос
    full_messages = [
        {
            "role": "system",
            "content": formatted_prompt
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
        # Добавляем сообщения в память (теперь по каналу, а не по пользователю)
        memory_manager.add_message(channel_id, "user", content, user_id)
        memory_manager.add_message(channel_id, "assistant", response, user_id)
        
        # Сохраняем память
        memory_manager.save_memory()
        
        # Отправляем ответ
        await message.reply(response)
        logger.info(f'Отправлен ответ пользователю {message.author.name}')
    else:
        await message.channel.send("Извините, я столкнулся с проблемой при генерации ответа. Попробуйте позже.")
        logger.error(f'Не удалось получить ответ для пользователя {message.author.name}')

# Команда для очистки памяти канала
@bot.command(name='clear')
async def clear_memory(ctx):
    """Очищает память бота для текущего канала"""
    channel_id = str(ctx.channel.id)
    memory_manager.clear_memory(channel_id)
    memory_manager.save_memory()
    await ctx.send(f"Память для канала {ctx.channel.mention} очищена!")

# Команда для информации о памяти
@bot.command(name='memory')
async def show_memory(ctx):
    """Показывает информацию о памяти чата"""
    channel_id = str(ctx.channel.id)
    summary = memory_manager.get_chat_summary(channel_id)
    
    if summary:
        response = f"📊 **Статистика чата {ctx.channel.name}**\n"
        response += f"💬 Сообщений: {summary['message_count']}/{MAX_MEMORY_SIZE}\n"
        response += f"👥 Участников: {summary['unique_users']}\n"
        
        if summary['topics']:
            response += f"📌 Темы: {', '.join(summary['topics'])}\n"
        
        if summary['important_messages_count'] > 0:
            response += f"⭐ Важных сообщений: {summary['important_messages_count']}\n"
        
        if summary['action_items_count'] > 0:
            response += f"📋 Задач: {summary['action_items_count']}\n"
        
        response += f"⏱️ Активность: {summary['activity_duration']}"
        await ctx.send(response)
    else:
        await ctx.send("Память для этого канала пуста.")

# Команда для показа важных сообщений
@bot.command(name='important')
async def show_important(ctx):
    """Показывает важные сообщения в чате"""
    channel_id = str(ctx.channel.id)
    important_messages = memory_manager.get_important_messages(channel_id)
    
    if important_messages:
        response = "🔍 **Важные моменты в чате:**\n"
        for i, msg in enumerate(important_messages[-3:], 1):  # Показываем последние 3
            user = f"<@{msg['user_id']}>" if msg['user_id'] else "Неизвестно"
            response += f"{i}. {user}: {msg['content'][:100]}...\n"
        await ctx.send(response)
    else:
        await ctx.send("В этом чате пока нет важных сообщений.")

# Команда для показа задач
@bot.command(name='tasks')
async def show_tasks(ctx):
    """Показывает список задач из чата"""
    channel_id = str(ctx.channel.id)
    action_items = memory_manager.get_action_items(channel_id)
    
    if action_items:
        response = "📋 **Список задач из чата:**\n"
        for i, task in enumerate(action_items, 1):
            response += f"{i}. {task}\n"
        await ctx.send(response)
    else:
        await ctx.send("В этом чате пока нет выявленных задач.")

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
            import prompts
            importlib.reload(memory)
            importlib.reload(openrouter_client)
            importlib.reload(prompts)
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
