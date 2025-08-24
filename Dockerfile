# === Этап 1: базовый Python + Poetry ===
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3 \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc curl libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# === Этап 2: установка зависимостей ===
FROM base AS deps

COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# === Этап 3: сборка и запуск ===
FROM deps AS runtime

COPY . /app

# Статическая папка (если надо)
RUN mkdir -p /app/staticfiles /app/media

# Открываем порт
EXPOSE 8000

# Команда запуска: миграции, статика, gunicorn
CMD bash -c "python manage.py migrate --noinput && \
             python manage.py collectstatic --noinput && \
             gunicorn habit_tracker.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120"
