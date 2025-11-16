# Requirements Document

## Introduction

Телеграм-бот для получения прогноза погоды по геолокации пользователя. Бот принимает локацию от пользователя и возвращает актуальный прогноз погоды, используя API Яндекс.Погоды.

## Glossary

- **TelegramBot**: Система бота для мессенджера Telegram
- **User**: Пользователь мессенджера Telegram, взаимодействующий с ботом
- **Location**: Географические координаты (широта и долгота), отправленные пользователем
- **WeatherAPI**: API Яндекс.Погоды для получения данных о погоде
- **WeatherForecast**: Данные о текущей погоде (температура, описание, влажность, скорость ветра)

## Requirements

### Requirement 1

**User Story:** Как пользователь, я хочу отправить свою геолокацию боту, чтобы получить прогноз погоды для моего местоположения

#### Acceptance Criteria

1. WHEN User отправляет Location через Telegram, THE TelegramBot SHALL принять координаты (широту и долготу)
2. THE TelegramBot SHALL поддерживать стандартный формат геолокации Telegram
3. IF User отправляет некорректные данные локации, THEN THE TelegramBot SHALL отправить сообщение об ошибке с инструкцией
4. THE TelegramBot SHALL обрабатывать запрос в течение 5 секунд с момента получения Location

### Requirement 2

**User Story:** Как пользователь, я хочу получить актуальный прогноз погоды, чтобы знать текущие погодные условия в моей локации

#### Acceptance Criteria

1. WHEN TelegramBot получает Location, THE TelegramBot SHALL отправить запрос к WeatherAPI с координатами
2. THE TelegramBot SHALL получить WeatherForecast с температурой, описанием погоды, влажностью и скоростью ветра
3. THE TelegramBot SHALL форматировать WeatherForecast в читаемое текстовое сообщение
4. THE TelegramBot SHALL отправить отформатированный WeatherForecast пользователю User
5. IF WeatherAPI недоступен, THEN THE TelegramBot SHALL отправить сообщение об ошибке User

### Requirement 3

**User Story:** Как пользователь, я хочу получить приветственное сообщение при запуске бота, чтобы понять, как им пользоваться

#### Acceptance Criteria

1. WHEN User отправляет команду /start, THE TelegramBot SHALL отправить приветственное сообщение
2. THE TelegramBot SHALL включить в приветственное сообщение инструкцию по отправке геолокации
3. WHEN User отправляет команду /help, THE TelegramBot SHALL отправить справочное сообщение с описанием функций

### Requirement 4

**User Story:** Как администратор, я хочу безопасно хранить API ключи, чтобы защитить доступ к сервисам

#### Acceptance Criteria

1. THE TelegramBot SHALL использовать переменные окружения для хранения API ключа Telegram
2. THE TelegramBot SHALL использовать переменные окружения для хранения API ключа Яндекс.Погоды
3. THE TelegramBot SHALL не включать API ключи в исходный код
4. IF API ключи отсутствуют при запуске, THEN THE TelegramBot SHALL вывести сообщение об ошибке и завершить работу

### Requirement 5

**User Story:** Как администратор, я хочу видеть логи работы бота, чтобы отслеживать его работу и диагностировать проблемы

#### Acceptance Criteria

1. THE TelegramBot SHALL логировать все входящие запросы от User
2. THE TelegramBot SHALL логировать все запросы к WeatherAPI
3. THE TelegramBot SHALL логировать все ошибки с детальной информацией
4. THE TelegramBot SHALL использовать структурированный формат логирования с временными метками
### Requirement 6

**User Story:** Как администратор, я хочу ограничить использование бота только указанным списком пользователей, чтобы контролировать доступ к сервису

#### Acceptance Criteria

1. THE TelegramBot SHALL использовать переменную окружения для хранения списка разрешенных User ID
2. WHEN User отправляет любую команду или Location, THE TelegramBot SHALL проверить, находится ли User ID в списке разрешенных
3. IF User ID не находится в списке разрешенных, THEN THE TelegramBot SHALL отправить сообщение о запрете доступа и игнорировать запрос
4. THE TelegramBot SHALL логировать все попытки несанкционированного доступа с указанием User ID
5. IF список разрешенных пользователей пуст или не задан, THEN THE TelegramBot SHALL разрешить доступ всем пользователям

### Requirement 7

**User Story:** Как пользователь, я хочу иметь возможность быстро запросить новый прогноз для последней использованной локации через интерактивную кнопку, чтобы не отправлять геолокацию повторно

#### Acceptance Criteria

1. WHEN TelegramBot отправляет WeatherForecast пользователю User, THE TelegramBot SHALL добавить интерактивную кнопку с текстом "Получить новый прогноз"
2. THE TelegramBot SHALL сохранить последнюю Location для каждого User
3. WHEN User нажимает кнопку "Получить новый прогноз", THE TelegramBot SHALL использовать сохраненную Location для запроса актуального WeatherForecast
4. THE TelegramBot SHALL отправить обновленный WeatherForecast с новой интерактивной кнопкой "Получить новый прогноз"
5. IF сохраненная Location для User отсутствует, THEN THE TelegramBot SHALL отправить сообщение с просьбой отправить геолокацию
