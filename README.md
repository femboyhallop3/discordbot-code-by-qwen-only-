"# 🤖 Discord AI Agent with DeepSeek

A powerful Discord bot using OpenRouter and DeepSeek for intelligent conversations with advanced memory capabilities.

## ✨ Features

- 🤖 **Smart AI**: Uses DeepSeek via OpenRouter API
- 💬 **Shared Chat Memory**: Remembers conversation history for entire channels
- 👥 **User Participation Tracking**: Monitors each user's contribution
- 📌 **Topic Detection**: Automatically identifies discussion topics
- ⭐ **Important Message Detection**: Identifies and stores key moments
- 📋 **Task Tracking**: Extracts tasks and actions from conversations
- 🧠 **Advanced Prompts**: Flexible prompt system with context awareness
- 🎯 **Smart Mentions**: Only responds when mentioned
- 🔧 **Easy Configuration**: Simple setup via config.py

## 📋 Requirements

- Python 3.8+
- Discord Bot Token
- OpenRouter API Key

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/discord-agent.git
cd discord-agent
```

### 2. Install dependencies

```bash
pip install -r discord_agent/requirements.txt
```

### 3. Configure the bot

The bot supports two configuration methods:

**Method 1: Environment variables (RECOMMENDED)**
1. Create a `.env` file in the `discord_agent` directory
2. Add your tokens:

```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

**Method 2: Direct editing of config.py**
Edit `discord_agent/config.py` and replace the placeholder values:

```python
DISCORD_BOT_TOKEN = "your_discord_bot_token_here"
OPENROUTER_API_KEY = "your_openrouter_api_key_here"
```

**Important notes:**
- The bot automatically loads from `.env` file if it exists
- Environment variables take precedence over config.py values
- Never commit your `.env` file to version control
- See `env_example.txt` for the template format

### 4. Run the bot

```bash
cd discord_agent
python bot.py
```

## 📖 Usage

### Mention the bot

Simply mention the bot in a channel:

```
@DeepBot Hello! How are you?
```

### Commands

- `!clear` - Clear memory for the current channel
- `!memory` - Show chat statistics and memory info
- `!important` - Show important messages in the chat
- `!tasks` - Show list of tasks extracted from the chat
- `!reload` - Reload modules (for developers)

## 🏗️ Project Structure

```
discord_agent/
├── bot.py                 # Main bot file
├── config.py             # Configuration settings
├── memory.py             # Memory system
├── openrouter_client.py  # OpenRouter API client
├── prompts.py            # Prompt management system
├── requirements.txt      # Dependencies
├── memory.json           # Memory storage (auto-generated)
└── README.md            # Project documentation
```

## 🔑 Getting API Keys

### Discord Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" tab and click "Add Bot"
4. Copy the token

### OpenRouter API Key
1. Register at [OpenRouter.ai](https://openrouter.ai/)
2. Go to API Keys section
3. Create a new API key

## 🧠 Memory System

The bot uses an advanced `MemoryManager` for conversation history:
- Each channel has its own memory
- Stores up to 50 messages per channel
- Automatically saves to `memory.json`
- Loads memory on startup
- Tracks topics, important messages, and tasks

## 🛠️ Configuration

In `config.py` you can customize:
- `MODEL_NAME` - Model name (default: deepseek/deepseek-v3.2)
- `MAX_MEMORY_SIZE` - Maximum messages in memory
- `IMPORTANT_MESSAGE_INDICATORS` - Keywords for important message detection

Available models on OpenRouter:
- `deepseek/deepseek-chat`
- `deepseek/deepseek-coder`
- `meta-llama/llama-3-8b-instruct`
- And many more...

## 🤝 Contributing

Contributions are welcome! For changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgements

- [OpenRouter](https://openrouter.ai/) for providing access to multiple models
- [Discord.py](https://discordpy.readthedocs.io/) for the excellent library
- [DeepSeek](https://www.deepseek.com/) for the powerful AI models

---

**Enjoy using the Discord AI Agent! 🎉**" 
