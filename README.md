# Habit Tracker

> 🧱 _"Если учебное заведение требует выполнения DevOps-требований,  
> но не предоставляет удалённого сервера — мы не паникуем._  
> **Мы строим инфраструктуру сами. На зубах."_

Полноценный трекер полезных привычек с Telegram-ботом, Celery-задачами и настоящим CI/CD-пайплайном.  
Настроено вручную на Ubuntu-сервере в Yandex Cloud. Django + DRF + PostgreSQL + Gunicorn + SSH-деплой.

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

Проект содержит CI/CD workflow `.github/workflows/deploy.yml`.

Workflow выполняет:

- установку зависимостей через poetry,
- запуск тестов (`pytest`) с переменными из GitHub Secrets,
- деплой на реальный удалённый сервер через `ssh-action`.

**✅ Всё работает. Не имитация.**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - develop
      - main
      - master
      - feature/deploy_ci_cd

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

1. Установите [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/).
2. В терминале перейдите в корневую директорию проекта.
3. Выполните команду:

```bash
docker-compose up --build
```

---

## ✅ Проверка работоспособности

- **Бэкенд Django**: `http://localhost:8000`
- **Swagger-документация**: `http://localhost:8000/swagger/`
- **PostgreSQL**: подключение с параметрами из `.env`
- **Redis**: 

```bash
docker exec -it <redis_container_name> redis-cli ping
```

Ожидаемый ответ: `PONG`

---

## 📱 Telegram

Создай бота через [@BotFather](https://t.me/BotFather), получи токен и вставь в `.env`.  
Telegram ID можно узнать через бота `@userinfobot`.

Бот отправляет напоминания по расписанию привычек.

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

Документация: `http://localhost:8000/swagger/`

---

## ✅ Валидации привычек

- ⛔ Нельзя указать одновременно награду и связанную привычку
- ⛔ Время выполнения ≤ 120 секунд
- ⛔ Периодичность ≥ 1 раз в 7 дней
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

- 👤 Пользователь может управлять только своими привычками
- 🌍 Публичные привычки доступны для чтения всем

---

## 🎯 Курсовые критерии — всё реализовано:

- ✅ CORS
- ✅ .env и переменные окружения
- ✅ Валидаторы и валидации модели
- ✅ Swagger-документация
- ✅ Права доступа и ограничения
- ✅ Celery + Telegram
- ✅ Тесты ≥ 90%
- ✅ Flake8 = 100%
- ✅ Docker + docker-compose
- ✅ CI/CD Workflow (GitHub Actions)
- ✅ Реальное развертывание на сервере

---

## 📚 Автор

Проект выполнен в рамках учебной курсовой работы.  
**Автор: Каратеев Виктор**
