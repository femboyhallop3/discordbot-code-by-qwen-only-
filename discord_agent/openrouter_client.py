"""
Модуль для работы с OpenRouter API
Интеграция с DeepSeek
"""
import requests
import json
from typing import List, Dict, Optional
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenRouterClient:
    def __init__(self, api_key: str, model_name: str = "deepseek/deepseek-chat"):
        self.api_key = api_key
        self.model_name = model_name
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
    
    def generate_response(self, messages: List[Dict[str, str]], user_id: str = "default") -> Optional[str]:
        """
        Генерирует ответ от DeepSeek через OpenRouter
        
        Args:
            messages: Список сообщений в формате [{"role": "user", "content": "..."}, ...]
            user_id: ID пользователя для логирования
            
        Returns:
            Строка с ответом модели или None при ошибке
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/yourusername/discord-agent",  # Для рейтинга
                "X-Title": "Discord AI Agent"
            }
            
            payload = {
                "model": self.model_name,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            logger.info(f"Отправка запроса к OpenRouter для пользователя {user_id}")
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Извлекаем ответ от модели
            if result.get('choices'):
                return result['choices'][0]['message']['content']
            else:
                logger.error(f"Нет выборок в ответе: {result}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе к OpenRouter: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга ответа: {e}")
            return None
