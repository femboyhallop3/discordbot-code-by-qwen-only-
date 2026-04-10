"""
Модуль памяти для AI агента
Хранит историю взаимодействий с пользователями
"""
from collections import deque
from typing import List, Dict, Optional
import json
import os

class MemoryManager:
    def __init__(self, max_size: int = 10, storage_file: str = "memory.json"):
        self.max_size = max_size
        self.storage_file = storage_file
        self.chat_history: Dict[str, deque] = {}  # user_id -> deque of messages
        self.load_memory()
    
    def add_message(self, user_id: str, role: str, content: str) -> None:
        """Добавляет сообщение в память"""
        if user_id not in self.chat_history:
            self.chat_history[user_id] = deque(maxlen=self.max_size)
        
        self.chat_history[user_id].append({
            "role": role,
            "content": content,
            "timestamp": str(__import__('datetime').datetime.now())
        })
    
    def get_history(self, user_id: str) -> List[Dict[str, str]]:
        """Получает историю сообщений для пользователя"""
        if user_id in self.chat_history:
            return list(self.chat_history[user_id])
        return []
    
    def clear_memory(self, user_id: str) -> None:
        """Очищает память для конкретного пользователя"""
        if user_id in self.chat_history:
            self.chat_history[user_id].clear()
    
    def save_memory(self) -> None:
        """Сохраняет память в файл"""
        data = {
            user_id: list(messages) 
            for user_id, messages in self.chat_history.items()
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
                    self.chat_history = {
                        user_id: deque(messages, maxlen=self.max_size)
                        for user_id, messages in data.items()
                    }
            except Exception as e:
                print(f"Ошибка загрузки памяти: {e}")
                self.chat_history = {}

# Глобальный экземпляр менеджера памяти
memory_manager = MemoryManager()
