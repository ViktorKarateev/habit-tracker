# Habit Tracker

Трекер полезных привычек с Telegram-уведомлениями, асинхронной рассылкой через Celery и REST API. Реализован на Django + DRF. Курсовой проект.

---

## 📦 Стек технологий

- Python 3.11+
- Django / DRF
- PostgreSQL
- Redis
- Celery + celery-beat
- Telegram Bot API
- Swagger (drf-yasg)
- JWT (SimpleJWT)
- poetry
- Flake8 / coverage

---

## 🚀 Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/yourname/habit-tracker.git
cd habit-tracker
```

### 2. Установить зависимости

```bash
poetry install
```

### 3. Настроить переменные окружения

Создай файл `.env` на основе `.env.example`:

```
DEBUG=True
SECRET_KEY=your-secret
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=habit_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://localhost:6379/0

BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 4. Провести миграции и создать суперпользователя

```bash
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
```

### 5. Запуск Celery + Beat

**В отдельном терминале:**

```bash
poetry run celery -A habit_tracker worker -l info
poetry run celery -A habit_tracker beat -l info
```

---

## 📱 Telegram

Создай бота через [@BotFather](https://t.me/BotFather), получи токен, вставь в `.env` (`BOT_TOKEN`).  
Твой Telegram ID (`TELEGRAM_CHAT_ID`) можно узнать через бота `@userinfobot`.

Уведомления отправляются по расписанию привычек через Telegram API.

---

## 🛠 API эндпоинты

| Метод | Путь                         | Описание                        |
|-------|------------------------------|---------------------------------|
| POST  | /auth/users/                 | Регистрация                     |
| POST  | /auth/jwt/create/            | Авторизация (JWT)              |
| GET   | /habits/                     | Список привычек пользователя    |
| GET   | /habits/public/              | Список публичных привычек       |
| POST  | /habits/                     | Создание привычки               |
| PUT   | /habits/{id}/                | Обновление привычки             |
| DELETE| /habits/{id}/                | Удаление привычки               |

Полная документация:  
📄 Swagger: `http://localhost:8000/swagger/`

---

## ✅ Валидации привычек

- ⛔ Нельзя указать одновременно награду и связанную привычку
- ⛔ Время выполнения ≤ 120 секунд
- ⛔ Периодичность не реже 1 раза в 7 дней
- ⛔ Связанная привычка должна быть приятной
- ⛔ Приятная привычка не может иметь вознаграждения

---

## 🧪 Тестирование

```bash
poetry run coverage run manage.py test
poetry run coverage report -m
```

✅ Покрытие ≥ 90%  
✅ Flake8 = 100%

---

## 🛡 Права доступа

- 👤 Пользователь имеет доступ только к своим привычкам (CRUD)
- 🌍 Публичные привычки видны всем, но нельзя редактировать

---

## 🎯 Курсовые критерии — всё реализовано:

- ✅ CORS
- ✅ Переменные окружения
- ✅ Модель с валидацией
- ✅ Swagger-документация
- ✅ Права доступа и валидаторы
- ✅ Celery и Telegram
- ✅ Покрытие тестами ≥ 80%
- ✅ Flake8 = 100%

---

## 📚 Автор

Проект выполнен в рамках учебной курсовой работы.
