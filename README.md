# Django_weather_project - это пет-проект с использованием Django и стороннего API, в частности openweathermap и yandex API геосаджер и API Геокодер

## Установка

1. **Клонируйте репозиторий:**

 - git clone https://github.com/archibaldlazarevich/Django_weather_project
 - cd Django_weather_project

2. **Установите зависимости:**

 - pip install poetry

 - poetry install --no-root

3. **Настройте переменные окружения:**
  Создайте файл `.env` используя .env.template и ваши API-key для Яндекс геокодера и openweathermap:

 - OPENWEATHER_API_KEY=your_openweathermap_key
 - YANDEX_API_KEY=your_yandex_api_key

4. **Запуск через Docker:**
 - Запуск:
    docker compose up --build
 - Остановка:
    docker compose down
    
5. **Запуск локально:**
 - Произведите миграции:
    python manage.py migrate
 - Создайте суперпользователя(при необходимости):
    python manage.py createsuperuser
 - Запустите сервер:
    python manage.py runserver



---

## Архитектура и функционал
- Регистрация и аутентификация пользователей через Django.

- После входа доступен поиск прогноза погоды по названию населённого пункта или выбор на Яндекс.Карте.

- Прогноз на текущий момент и последующие 5 дней.

- Интеграция карт (описать, каким образом подключены Яндекс.Карты).

- Использование OpenWeatherMap для получения погодных данных, Яндекс Геокодер — для определения координат по названию города..


---

## Требования

- Python 3.10+
- django 5.2.x
- (другие зависимости — см. pyproject.toml)

---

## Использование
- Зарегистрируйтесь на сайте.

- Зайдите в личный кабинет.

- Введите название населённого пункта или выберите его на карте, чтобы получить прогноз.

---
## Лицензия и API-ключи

- Для работы необходимы личные API-ключи OpenWeatherMap и Яндекс. Получите их на официальных сайтах.

---

## Авторы

- Артур Лазаревич [archibaldlazarevich](https://github.com/archibaldlazarevich)

- почта [compact_00@mail.ru](mailto:compact_00@mail.ru)
---
