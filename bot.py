"""
Основной модуль Telegram Weather Bot
Инициализирует бота и запускает polling
"""
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import Config
from handlers import router, AccessControlMiddleware


async def main() -> None:
    """
    Инициализация и запуск бота
    """
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    # Загрузка и валидация конфигурации
    logger.info("Загрузка конфигурации...")
    Config.load()
    Config.validate()
    
    logger.info("Конфигурация успешно загружена")
    
    # Инициализация бота и диспетчера
    bot = Bot(token=Config.TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    
    # Регистрация middleware для контроля доступа
    router.message.middleware(AccessControlMiddleware())
    
    # Регистрация роутера с обработчиками
    dp.include_router(router)
    
    logger.info("Бот запускается...")
    
    try:
        # Запуск polling
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при работе бота: {e}", exc_info=True)
    finally:
        # Корректное завершение
        logger.info("Остановка бота...")
        await bot.session.close()
        logger.info("Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}", file=sys.stderr)
        sys.exit(1)
