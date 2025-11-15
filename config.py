"""
Configuration module for Telegram Weather Bot.
Loads and validates environment variables.
"""
import os
import sys
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration class for managing environment variables."""
    
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    YANDEX_WEATHER_API_KEY: Optional[str] = None
    ALLOWED_USER_IDS: list[int] = []
    
    @classmethod
    def load(cls) -> None:
        """
        Load configuration from environment variables.
        Reads TELEGRAM_BOT_TOKEN, YANDEX_WEATHER_API_KEY, and ALLOWED_USER_IDS from .env file.
        """
        load_dotenv()
        
        cls.TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        cls.YANDEX_WEATHER_API_KEY = os.getenv('YANDEX_WEATHER_API_KEY')
        
        # Parse ALLOWED_USER_IDS from comma-separated string
        allowed_ids_str = os.getenv('ALLOWED_USER_IDS', '')
        if allowed_ids_str.strip():
            try:
                cls.ALLOWED_USER_IDS = [int(uid.strip()) for uid in allowed_ids_str.split(',') if uid.strip()]
            except ValueError:
                print("⚠️ Предупреждение: ALLOWED_USER_IDS содержит некорректные значения. Используется пустой список.", file=sys.stderr)
                cls.ALLOWED_USER_IDS = []
        else:
            cls.ALLOWED_USER_IDS = []
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate that all required configuration parameters are present.
        
        Returns:
            bool: True if all required parameters are present, False otherwise.
        
        Raises:
            SystemExit: If required API keys are missing.
        """
        missing_keys = []
        
        if not cls.TELEGRAM_BOT_TOKEN:
            missing_keys.append('TELEGRAM_BOT_TOKEN')
        
        if not cls.YANDEX_WEATHER_API_KEY:
            missing_keys.append('YANDEX_WEATHER_API_KEY')
        
        if missing_keys:
            error_message = (
                f"❌ Ошибка конфигурации: отсутствуют обязательные переменные окружения:\n"
                f"{', '.join(missing_keys)}\n\n"
                f"Пожалуйста, создайте файл .env и добавьте необходимые API ключи.\n"
                f"Пример можно найти в файле .env.example"
            )
            print(error_message, file=sys.stderr)
            sys.exit(1)
        
        return True
    
    @classmethod
    def is_user_allowed(cls, user_id: int) -> bool:
        """
        Check if a user is allowed to use the bot.
        
        Args:
            user_id: Telegram User ID
            
        Returns:
            bool: True if access is allowed (list is empty or user_id is in the list)
        """
        # If the list is empty, allow all users
        if not cls.ALLOWED_USER_IDS:
            return True
        
        # Otherwise, check if user_id is in the allowed list
        return user_id in cls.ALLOWED_USER_IDS
