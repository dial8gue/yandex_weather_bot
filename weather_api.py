"""
Модуль для работы с Яндекс.Погода API
"""
import asyncio
import logging
from typing import Optional
import aiohttp


logger = logging.getLogger(__name__)


class WeatherAPIError(Exception):
    """Кастомное исключение для ошибок Weather API"""
    pass


class WeatherAPIClient:
    """Клиент для асинхронного взаимодействия с Яндекс.Погода API"""
    
    BASE_URL = "https://api.weather.yandex.ru/v2/forecast"
    
    def __init__(self, api_key: str):
        """
        Инициализация клиента с API ключом
        
        Args:
            api_key: API ключ Яндекс.Погоды
        """
        self.api_key = api_key
        self._session: Optional[aiohttp.ClientSession] = None
    
    @property
    def session(self) -> aiohttp.ClientSession:
        """Получить или создать aiohttp сессию"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def get_weather(self, lat: float, lon: float) -> dict:
        """
        Получить текущую погоду по координатам
        
        Args:
            lat: Широта
            lon: Долгота
            
        Returns:
            dict: Данные о погоде
            
        Raises:
            WeatherAPIError: При ошибке запроса к API
        """
        headers = {
            "X-Yandex-API-Key": self.api_key
        }
        
        params = {
            "lat": lat,
            "lon": lon,
            "lang": "ru_RU",
            "limit": 1,
            "hours": "false",
            "extra": "false"
        }
        
        try:
            logger.info(f"Запрос погоды для координат: lat={lat}, lon={lon}")
            
            async with self.session.get(
                self.BASE_URL,
                headers=headers,
                params=params,
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Успешно получены данные о погоде")
                    return data
                
                elif response.status == 403:
                    logger.error("Ошибка авторизации: неверный API ключ")
                    raise WeatherAPIError("Ошибка авторизации: проверьте API ключ")
                
                elif response.status == 404:
                    logger.error(f"Локация не найдена: lat={lat}, lon={lon}")
                    raise WeatherAPIError("Не удалось найти погоду для указанной локации")
                
                elif response.status == 500:
                    logger.error("Внутренняя ошибка сервера Яндекс.Погоды")
                    raise WeatherAPIError("Сервис погоды временно недоступен")
                
                else:
                    logger.error(f"Неожиданный статус ответа: {response.status}")
                    raise WeatherAPIError(f"Ошибка API: статус {response.status}")
        
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка сети при запросе к Weather API: {e}")
            raise WeatherAPIError(f"Ошибка подключения к сервису погоды: {e}")
        
        except asyncio.TimeoutError:
            logger.error("Превышено время ожидания ответа от Weather API")
            raise WeatherAPIError("Превышено время ожидания ответа от сервиса погоды")
    
    async def close(self) -> None:
        """Закрыть aiohttp сессию"""
        if self._session and not self._session.closed:
            await self._session.close()
            logger.info("Weather API клиент закрыт")
