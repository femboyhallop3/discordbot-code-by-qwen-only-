# 🤖 Discord AI Агент с DeepSeek

Потрясающий Discord бот, использующий OpenRouter и DeepSeek для умных бесед!

## ✨ Особенности

- 🤖 **Умный AI**: Использует DeepSeek через OpenRouter API
- 💬 **Контекстная память**: Запоминает историю общения с каждым пользователем
- 🎯 **Умные упоминания**: Отвечает только когда его упоминают
- 🧠 **Гибкая память**: Хранит до 10 последних сообщений на пользователя
- 🔧 **Легко настраиваемый**: Простая конфигурация через config.py

## 📋 Требования

- Python 3.8+
- Discord Bot Token
- OpenRouter API Key

## 🚀 Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/yourusername/discord-agent.git
cd discord-agent
```

### 2. Установите зависимости

```bash
pip install -r requirements.txt
```

### 3. Настройте конфигурацию

Создайте файл `.env` в папке проекта:

```env
DISCORD_BOT_TOKEN=ваш_токен_бота
OPENROUTER_API_KEY=ваш_openrouter_api_ключ
DEVELOPER_ID=ваш_discord_id
```

### 4. Запустите бота

```bash
python bot.py
```

## 📖 Использование

### Упоминание бота

Просто упомяните бота в канале:

```
@DeepBot Привет! Как дела?
```

### Команды

- `!clear` - Очистить память для текущего пользователя
- `!memory` - Показать количество сообщений в памяти
- `!reload` - Перезагрузить модули (для разработчиков)

## 🏗️ Структура проекта

```
discord_agent/
├── bot.py                 # Основной файл бота
├── config.py             # Конфигурация
├── memory.py             # Система памяти
├── openrouter_client.py  # Клиент OpenRouter
├── requirements.txt      # Зависимости
├── .env                  # Переменные окружения (не включен в git)
├── memory.json           # Файл сохранения памяти (автоматически создается)
└── README.md
```

## 🔑 Получение токенов

### Discord Bot Token
1. Зайдите на [Discord Developer Portal](https://discord.com/developers/applications)
2. Создайте новое приложение
3. Перейдите во вкладку "Bot" и нажмите "Add Bot"
4. Скопируйте токен

### OpenRouter API Key
1. Зарегистрируйтесь на [OpenRouter.ai](https://openrouter.ai/)
2. Перейдите в раздел API Keys
3. Создайте новый API ключ

## 🧠 Как работает память?

Бот использует `MemoryManager` для хранения истории общения:
- Каждый пользователь имеет свою отдельную историю
- Хранится до 10 последних сообщений
- История сохраняется в `memory.json` автоматически
- При перезапуске бот загружает память из файла

## 🛠️ Настройка модели

В `config.py` вы можете изменить:
- `MODEL_NAME` - Имя модели (по умолчанию: deepseek/deepseek-chat)
- `MAX_MEMORY_SIZE` - Максимальное количество сообщений в памяти

Доступные модели на OpenRouter:
- `deepseek/deepseek-chat`
- `deepseek/deepseek-coder`
- `meta-llama/llama-3-8b-instruct`
- И многие другие...

## 🤝 Вклад

Приветствуются Pull Request'ы! Для изменений:

1. Создайте фork репозитория
2. Создайте ветку (`git checkout -b feature/AmazingFeature`)
3. Закоммитьте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📝 Лицензия

Этот проект лицензирован по лицензии MIT - см. файл LICENSE

## 🙏 Благодарности

- [OpenRouter](https://openrouter.ai/) за предоставление доступа к множеству моделей
- [Discord.py](https://discordpy.readthedocs.io/) за отличную библиотеку

---

**Приятного использования! 🎉**
