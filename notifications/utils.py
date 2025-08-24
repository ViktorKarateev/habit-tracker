import os  # noqa: F401
import requests
from django.conf import settings


TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN


def send_telegram_message(chat_id: str, text: str) -> bool:
    """Простая отправка сообщения через Telegram Bot API."""
    if not TELEGRAM_BOT_TOKEN:
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        resp = requests.post(url, json={"chat_id": chat_id, "text": text})
        return resp.status_code == 200
    except Exception:
        return False
