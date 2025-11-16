"""
Модуль для форматирования сообщений о погоде
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Словарь для перевода условий погоды на русский с эмодзи
CONDITION_EMOJI = {
    "clear": "☀️",
    "partly-cloudy": "⛅",
    "cloudy": "☁️",
    "overcast": "☁️",
    "drizzle": "🌦️",
    "light-rain": "🌧️",
    "rain": "🌧️",
    "moderate-rain": "🌧️",
    "heavy-rain": "⛈️",
    "continuous-heavy-rain": "⛈️",
    "showers": "🌧️",
    "wet-snow": "🌨️",
    "light-snow": "🌨️",
    "snow": "❄️",
    "snow-showers": "🌨️",
    "hail": "🌨️",
    "thunderstorm": "⛈️",
    "thunderstorm-with-rain": "⛈️",
    "thunderstorm-with-hail": "⛈️",
}

CONDITION_TRANSLATIONS = {
    "clear": "ясно",
    "partly-cloudy": "малооблачно",
    "cloudy": "облачно с прояснениями",
    "overcast": "пасмурно",
    "drizzle": "морось",
    "light-rain": "небольшой дождь",
    "rain": "дождь",
    "moderate-rain": "умеренно сильный дождь",
    "heavy-rain": "сильный дождь",
    "continuous-heavy-rain": "длительный сильный дождь",
    "showers": "ливень",
    "wet-snow": "дождь со снегом",
    "light-snow": "небольшой снег",
    "snow": "снег",
    "snow-showers": "снегопад",
    "hail": "град",
    "thunderstorm": "гроза",
    "thunderstorm-with-rain": "дождь с грозой",
    "thunderstorm-with-hail": "гроза с градом",
}


def format_weather_message(weather_data: dict) -> str:
    """
    Форматировать данные о погоде в читаемое сообщение
    
    Args:
        weather_data: Данные от Яндекс.Погода API
        
    Returns:
        str: Отформатированное сообщение с погодой
    """
    try:
        fact = weather_data.get("fact", {})
        
        # Получаем основные данные с обработкой отсутствующих полей
        temp = fact.get("temp")
        feels_like = fact.get("feels_like")
        condition = fact.get("condition", "")
        wind_speed = fact.get("wind_speed")
        humidity = fact.get("humidity")
        pressure_mm = fact.get("pressure_mm")
        
        # Формируем сообщение
        message_parts = []
        
        # Заголовок с эмодзи погоды
        condition_emoji = CONDITION_EMOJI.get(condition, "🌍")
        condition_text = CONDITION_TRANSLATIONS.get(condition, condition)
        message_parts.append(f"{condition_emoji} {condition_text.capitalize()}")
        message_parts.append("")
        
        # Температура
        if temp is not None:
            temp_sign = "+" if temp > 0 else ""
            message_parts.append(f"🌡️ Температура: {temp_sign}{temp}°C")
            
            if feels_like is not None:
                feels_sign = "+" if feels_like > 0 else ""
                message_parts.append(f"🤔 Ощущается как: {feels_sign}{feels_like}°C")
        
        # Влажность
        if humidity is not None:
            message_parts.append(f"💧 Влажность: {humidity}%")
        
        # Ветер
        if wind_speed is not None:
            message_parts.append(f"💨 Ветер: {wind_speed} м/с")
        
        # Давление
        if pressure_mm is not None:
            message_parts.append(f"🔽 Давление: {pressure_mm} мм рт.ст.")
        
        return "\n".join(message_parts)
    
    except Exception as e:
        # Если произошла ошибка при форматировании, возвращаем базовое сообщение
        return "⚠️ Не удалось отформатировать данные о погоде"


def create_refresh_keyboard() -> InlineKeyboardMarkup:
    """
    Создать inline клавиатуру с кнопкой "Получить новый прогноз"
    
    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопкой обновления прогноза
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🔄 Получить новый прогноз",
            callback_data="refresh_weather"
        )]
    ])
    return keyboard
