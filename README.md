# Habit Tracker

> 🧱 _"Если учебное заведение требует выполнения DevOps-требований,  
> но не предоставляет удалённого сервера — мы не паникуем._  
> **Мы строим инфраструктуру сами. На зубах."_

Полноценный трекер полезных привычек с Telegram-ботом, Celery-задачами и CI/CD-пайплайном.  
Настроено вручную на Ubuntu-сервере в Yandex Cloud. Django + DRF + PostgreSQL + Docker + Celery + Redis + GitHub Actions.

---

## 📦 Стек технологий
- Python 3.13+
- Django / DRF
- PostgreSQL (в Docker)
- Redis
- Celery + celery-beat
- Telegram Bot API
- Swagger (drf-yasg)
- JWT (SimpleJWT)
- Poetry
- Flake8 / coverage
- Docker + Docker Compose
- GitHub Actions (CI/CD)

---

## 🚀 Установка и запуск (локально, без Docker)
### 1. Клонировать репозиторий
git clone https://github.com/ViktorKarateev/habit-tracker.git
cd habit-tracker

### 2. Установить зависимости
poetry install

### 3. Настроить переменные окружения
Создайте файл `.env` на основе `.env.example`:
DEBUG=True
SECRET_KEY=your-secret
ALLOWED_HOSTS=127.0.0.1,localhost

# Для Docker-развертывания (PostgreSQL)
POSTGRES_DB=habit_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Локально можно использовать SQLite (по умолчанию)
REDIS_URL=redis://localhost:6379/0

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id

### 4. Провести миграции и создать суперпользователя
poetry run python manage.py migrate
poetry run python manage.py createsuperuser

### 5. Запуск Celery + Beat
**В отдельном терминале:**
poetry run celery -A habit_tracker worker -l info
poetry run celery -A habit_tracker beat -l info

---

## 🐙 CI/CD (GitHub Actions)
Файл: `.github/workflows/deploy.yml`

Workflow выполняет:
- установку зависимостей через poetry;
- линтинг (Flake8);
- запуск тестов (`pytest`);
- сборку Docker-образов;
- деплой на сервер через SSH.

**Обязательные GitHub Secrets:**
- SECRET_KEY
- SERVER_HOST
- SERVER_USER
- SSH_PRIVATE_KEY
- POSTGRES_USER
- POSTGRES_PASSWORD

**Основные шаги деплоя на сервер:**
cd /home/ubuntu/habit-tracker
git pull
docker-compose -f docker-compose.yaml down
docker-compose -f docker-compose.yaml build
docker-compose -f docker-compose.yaml up -d
docker-compose -f docker-compose.yaml run --rm web python manage.py migrate
docker-compose -f docker-compose.yaml run --rm web python manage.py collectstatic --noinput

---

## 📦 Запуск через Docker Compose
1. Установите [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/).
2. В терминале перейдите в корневую директорию проекта.
3. Выполните команду:
docker-compose -f docker-compose.yaml up --build

---

## ✅ Проверка работоспособности
- **Бэкенд Django**: http://130.193.35.145:8000
- **Swagger-документация**: http://130.193.35.145:8000/swagger/
- **PostgreSQL**: подключение с параметрами из `.env`
- **Redis**:
docker exec -it <redis_container_name> redis-cli ping
Ожидаемый ответ: PONG

---

## 📱 Telegram
Создай бота через [@BotFather](https://t.me/BotFather), получи токен и вставь его в `.env`.  
Telegram ID можно узнать через бота @userinfobot.

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

Документация: http://130.193.35.145:8000/swagger/

---

## ✅ Валидации привычек
- ⛔ Нельзя указать одновременно награду и связанную привычку
- ⛔ Время выполнения ≤ 120 секунд
- ⛔ Периодичность ≥ 1 раз в 7 дней
- ⛔ Связанная привычка должна быть приятной
- ⛔ Приятная привычка не может иметь вознаграждения

---

## 🧪 Тестирование
poetry run coverage run manage.py test
poetry run coverage report -m

✅ Покрытие ≥ 90%  
✅ Flake8 = 100%

---

## 🛡 Права доступа
- 👤 Пользователь может управлять только своими привычками
- 🌍 Публичные привычки доступны для чтения всем

---

## 📚 Автор
Проект выполнен в рамках учебной курсовой работы.  
**Автор: Каратеев Виктор**
