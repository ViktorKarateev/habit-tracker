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
- GitHub Actions (CI/CD)

---

## 🚀 Установка и запуск (локально без Docker)

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

## 🐙 CI/CD (GitHub Actions)

Проект содержит пример CI/CD workflow `.github/workflows/deploy.yml`.

Workflow выполняет:

- установку зависимостей через poetry,
- запуск тестов (`pytest`) с переменными из GitHub Secrets,
- (эмуляция) деплоя на сервер через `ssh-action` — **заглушка** (сервер отсутствует).

Пример используется для соответствия критериям курсовой.

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - develop
      - main
      - master

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Install dependencies
        run: poetry install

      - name: Run tests
        run: poetry run pytest
        env:
          DJANGO_SETTINGS_MODULE: habit_tracker.settings
          SECRET_KEY: ${{ secrets.SECRET_KEY }}
          DEBUG: True

      - name: Deploy to remote server
        if: success()
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /home/your_user/habit-tracker
            git pull
            source .venv/bin/activate
            poetry install
            python manage.py migrate
            sudo systemctl restart habit_tracker
```

---

## 📦 Запуск через Docker Compose

1. Установите [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/), если они ещё не установлены.
2. В терминале перейдите в корневую директорию проекта.
3. Выполните команду:

```bash
docker-compose up --build
```

После запуска все сервисы поднимутся автоматически.

---

### ✅ Проверка работоспособности

- **Бэкенд Django**: открой в браузере `http://localhost:8000`
- **Swagger-документация**: `http://localhost:8000/swagger/`
- **PostgreSQL**: подключись к базе через pgAdmin или другой клиент с параметрами из `.env`
- **Redis**: открой терминал и выполни:

```bash
docker exec -it <redis_container_name> redis-cli ping
```

Ожидаемый ответ: `PONG`

- **Celery / Beat**: логи отображаются в терминале. Убедись, что задачи запускаются без ошибок.

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
- ✅ Docker + docker-compose + инструкции по запуску
- ✅ CI/CD Workflow через GitHub Actions (эмуляция деплоя)

---

## 📚 Автор

Проект выполнен в рамках учебной курсовой работы.  
**Автор: Каратеев Виктор**
