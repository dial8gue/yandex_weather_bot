"""
Модуль для хранения последних локаций пользователей в памяти.
"""


class UserLocationStorage:
    """Хранилище последних локаций пользователей"""
    
    def __init__(self):
        """Инициализация хранилища с пустым словарем"""
        self._storage: dict[int, dict[str, float]] = {}
    
    def save_location(self, user_id: int, latitude: float, longitude: float) -> None:
        """
        Сохранить локацию пользователя
        
        Args:
            user_id: Telegram User ID
            latitude: Широта
            longitude: Долгота
        """
        self._storage[user_id] = {
            "latitude": latitude,
            "longitude": longitude
        }
    
    def get_location(self, user_id: int) -> tuple[float, float] | None:
        """
        Получить сохраненную локацию пользователя
        
        Args:
            user_id: Telegram User ID
            
        Returns:
            tuple[float, float] | None: (latitude, longitude) или None если не найдено
        """
        location_data = self._storage.get(user_id)
        if location_data is None:
            return None
        return (location_data["latitude"], location_data["longitude"])
