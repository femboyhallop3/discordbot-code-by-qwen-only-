"""
Модуль памяти для AI агента
Хранит историю взаимодействий с пользователями и чатом
"""
from collections import deque
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import json
import os
import re

class ChatMemory:
    """Память чата - общая для всего канала"""
    def __init__(self, max_size: int = 50):
        self.max_size = max_size
        self.messages: deque = deque(maxlen=max_size)
        self.topic_detection_threshold = 3  # Минимум сообщений для определения темы
        self.user_participation: Dict[str, int] = {}  # Количество сообщений каждого пользователя
        self.keywords: List[str] = []  # Ключевые слова из сообщений
        self.topics: List[str] = []  # Обнаруженные темы
        self.creation_time = datetime.now()
        self.important_messages: List[Dict] = []  # Важные сообщения (до 10)
        self.action_items: List[str] = []  # Список задач/действий
    
    def add_message(self, role: str, content: str, user_id: str = None) -> None:
        """Добавляет сообщение в память чата"""
        message_data = {
            "role": role,
            "content": content,
            "timestamp": str(datetime.now()),
            "user_id": user_id
        }
        self.messages.append(message_data)
        
        # Обновляем статистику участия
        if user_id:
            self.user_participation[user_id] = self.user_participation.get(user_id, 0) + 1
        
        # Извлекаем ключевые слова из сообщений
        self._extract_keywords(content)
        
        # Обновляем темы
        self._detect_topics()
        
        # Проверяем на важные сообщения
        self._detect_important_messages(message_data)
        
        # Проверяем на задачи/действия
        self._detect_action_items(content)
    
    def get_recent_messages(self, limit: int = 10) -> List[Dict]:
        """Получить последние N сообщений"""
        return list(self.messages)[-limit:]
    
    def get_context_for_user(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Получить контекст с учетом вклада пользователя"""
        messages = self.get_recent_messages(limit)
        # Добавляем информацию о вкладе пользователя
        for msg in messages:
            if msg.get("user_id") == user_id:
                msg["user_context"] = "Ваш вклад: " + str(self.user_participation.get(user_id, 0)) + " сообщений"
        return messages
    
    def _extract_keywords(self, content: str) -> None:
        """Извлечение ключевых слов из текста"""
        # Простая обработка - можно улучшить с помощью NLP
        words = re.findall(r'\b\w+\b', content.lower())
        # Фильтруем короткие слова и стоп-слова
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
                     'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'we', 'they'}
        keywords = [w for w in words if len(w) > 3 and w not in stop_words]
        self.keywords.extend(keywords)
        # Ограничиваем список ключевых слов
        if len(self.keywords) > 50:
            self.keywords = self.keywords[-50:]
    
    def _detect_topics(self) -> None:
        """Обнаружение тем на основе ключевых слов"""
        if len(self.messages) < self.topic_detection_threshold:
            return
        
        # Простая эвристика для определения тем
        common_keywords = set(self.keywords)
        if len(common_keywords) >= 2:
            self.topics = list(common_keywords)[:3]  # Берем до 3 тем
    
    def _detect_important_messages(self, message_data: Dict) -> None:
        """Обнаружение важных сообщений"""
        content = message_data["content"].lower()
        important_indicators = [
            "важно", "срочно", "внимание", "приоритет",
            "решение", "итог", "вывод", "результат"
        ]
        
        if any(indicator in content for indicator in important_indicators):
            self.important_messages.append(message_data)
            # Ограничиваем до 10 важных сообщений
            if len(self.important_messages) > 10:
                self.important_messages.pop(0)
    
    def _detect_action_items(self, content: str) -> None:
        """Обнаружение задач и действий"""
        # Ищем фразы, указывающие на задачи
        action_patterns = [
            r'\b(нужно|надо|требуется|сделать|организовать|планировать)\b',
            r'\b(задача|действие|план|мероприятие)\b',
            r'\b(сделать|выполнить|реализовать|организовать)\b'
        ]
        
        for pattern in action_patterns:
            if re.search(pattern, content.lower()):
                # Извлекаем предложение с задачей
                sentences = re.split(r'[.!?]', content)
                for sentence in sentences:
                    if re.search(pattern, sentence.lower()):
                        self.action_items.append(sentence.strip())
                        # Ограничиваем до 5 задач
                        if len(self.action_items) > 5:
                            self.action_items.pop(0)
                        break
    
    def get_summary(self) -> Dict:
        """Получить краткое описание текущего состояния чата"""
        return {
            "message_count": len(self.messages),
            "unique_users": len(self.user_participation),
            "topics": self.topics,
            "keywords": self.keywords[-10:],  # Последние 10 ключевых слов
            "activity_duration": str(datetime.now() - self.creation_time),
            "important_messages_count": len(self.important_messages),
            "action_items_count": len(self.action_items)
        }
    
    def get_important_messages(self) -> List[Dict]:
        """Получить список важных сообщений"""
        return self.important_messages
    
    def get_action_items(self) -> List[str]:
        """Получить список задач и действий"""
        return self.action_items
    
    def clear_memory(self) -> None:
        """Очистить всю память чата"""
        self.messages.clear()
        self.user_participation.clear()
        self.keywords.clear()
        self.topics.clear()
        self.important_messages.clear()
        self.action_items.clear()
        self.creation_time = datetime.now()

class MemoryManager:
    def __init__(self, max_size: int = 50, storage_file: str = "memory.json"):
        self.max_size = max_size
        self.storage_file = storage_file
        self.chat_memories: Dict[str, ChatMemory] = {}  # channel_id -> ChatMemory
        self.load_memory()
    
    def _get_chat_memory(self, channel_id: str) -> ChatMemory:
        """Получить память для канала (создать если нет)"""
        if channel_id not in self.chat_memories:
            self.chat_memories[channel_id] = ChatMemory(max_size=self.max_size)
        return self.chat_memories[channel_id]
    
    def add_message(self, channel_id: str, role: str, content: str, user_id: str = None) -> None:
        """Добавляет сообщение в память чата"""
        chat_memory = self._get_chat_memory(channel_id)
        chat_memory.add_message(role, content, user_id)
    
    def get_history(self, channel_id: str, user_id: str = None, limit: int = 10) -> List[Dict]:
        """Получает историю сообщений для канала"""
        chat_memory = self._get_chat_memory(channel_id)
        if user_id:
            return chat_memory.get_context_for_user(user_id, limit)
        return chat_memory.get_recent_messages(limit)
    
    def get_chat_summary(self, channel_id: str) -> Optional[Dict]:
        """Получить краткое описание чата"""
        if channel_id in self.chat_memories:
            return self.chat_memories[channel_id].get_summary()
        return None
    
    def get_important_messages(self, channel_id: str) -> List[Dict]:
        """Получить важные сообщения для канала"""
        if channel_id in self.chat_memories:
            return self.chat_memories[channel_id].get_important_messages()
        return []

    def get_action_items(self, channel_id: str) -> List[str]:
        """Получить задачи и действия для канала"""
        if channel_id in self.chat_memories:
            return self.chat_memories[channel_id].get_action_items()
        return []

    def clear_memory(self, channel_id: str) -> None:
        """Очищает память для конкретного канала"""
        if channel_id in self.chat_memories:
            self.chat_memories[channel_id].clear_memory()

    def save_memory(self) -> None:
        """Сохраняет память в файл"""
        data = {
            channel_id: {
                "messages": list(memory.messages),
                "user_participation": memory.user_participation,
                "keywords": memory.keywords,
                "topics": memory.topics,
                "important_messages": memory.important_messages,
                "action_items": memory.action_items,
                "creation_time": str(memory.creation_time)
            }
            for channel_id, memory in self.chat_memories.items()
        }
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения памяти: {e}")
    
    def load_memory(self) -> None:
        """Загружает память из файла"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"Загружены данные из {self.storage_file}: {type(data)}")
                    
                    # Проверяем, что data является словарем
                    if not isinstance(data, dict):
                        print("Ошибка: файл памяти содержит некорректные данные")
                        self.chat_memories = {}
                        return
                        
                    # Проверяем, старая ли это структура (с ключами channels, users и т.д.)
                    if "channels" in data and "users" in data:
                        # Это старая структура, конвертируем ее в новую
                        print("Обнаружена старая структура памяти, выполняем конвертацию...")
                        self.chat_memories = {}
                        # Для старой структуры просто создаем пустую память
                        # (данные из старой структуры не совместимы с новой)
                        return
                        
                    # Новая структура: channel_id -> memory_data
                    self.chat_memories = {}
                    print(f"Начинаем обработку {len(data)} каналов...")
                    for channel_id, memory_data in data.items():
                        print(f"Обработка канала {channel_id}: {type(memory_data)}")
                        
                        # Проверяем, что memory_data является словарем
                        if not isinstance(memory_data, dict):
                            print(f"Ошибка: некорректные данные для канала {channel_id}")
                            # Попробуем конвертировать список в словарь, если это возможно
                            if isinstance(memory_data, list):
                                print(f"  Попытка конвертации списка в словарь...")
                                # Если это список сообщений, создадим минимальную память
                                try:
                                    memory = ChatMemory(max_size=self.max_size)
                                    # Предполагаем, что это список сообщений
                                    messages = []
                                    for item in memory_data:
                                        if isinstance(item, dict):
                                            messages.append(item)
                                        elif isinstance(item, str):
                                            messages.append({
                                                "role": "user",
                                                "content": item,
                                                "timestamp": str(datetime.now()),
                                                "user_id": None
                                            })
                                    memory.messages = deque(messages, maxlen=self.max_size)
                                    self.chat_memories[channel_id] = memory
                                    print(f"  Канал {channel_id} успешно конвертирован")
                                except Exception as e:
                                    print(f"  Ошибка конвертации: {e}")
                            continue
                            
                        memory = ChatMemory(max_size=self.max_size)
                        
                        # Берем сообщения и преобразуем в deque
                        messages = memory_data.get("messages", []) if isinstance(memory_data, dict) else []
                        print(f"  Сообщения: {len(messages)}")
                        memory.messages = deque(messages, maxlen=self.max_size)
                        
                        # Безопасно получаем остальные данные
                        memory.user_participation = memory_data.get("user_participation", {}) if isinstance(memory_data, dict) else {}
                        memory.keywords = memory_data.get("keywords", []) if isinstance(memory_data, dict) else []
                        memory.topics = memory_data.get("topics", []) if isinstance(memory_data, dict) else []
                        memory.important_messages = memory_data.get("important_messages", []) if isinstance(memory_data, dict) else []
                        memory.action_items = memory_data.get("action_items", []) if isinstance(memory_data, dict) else []
                        
                        # Безопасно получаем время создания
                        creation_time_str = memory_data.get("creation_time", str(datetime.now())) if isinstance(memory_data, dict) else str(datetime.now())
                        try:
                            memory.creation_time = datetime.fromisoformat(creation_time_str)
                        except ValueError:
                            memory.creation_time = datetime.now()
                            
                        self.chat_memories[channel_id] = memory
                        print(f"  Канал {channel_id} успешно загружен")
            except Exception as e:
                print(f"Ошибка загрузки памяти: {e}")
                import traceback
                traceback.print_exc()
                self.chat_memories = {}

# Глобальный экземпляр менеджера памяти
memory_manager = MemoryManager()
