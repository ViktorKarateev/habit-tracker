from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from habits.models import Habit
from notifications.utils import send_telegram_message

@shared_task
def send_due_habits():
    """
    Отправляет напоминания за текущую минуту с допуском ±1 минута,
    учитывает периодичность и не шлёт повторно в тот же день.
    """
    tz_now = timezone.localtime()
    today = tz_now.date()

    # Окно: с предыдущей минуты включительно до следующей (не включая)
    minute_start = tz_now.replace(second=0, microsecond=0)
    window_start = minute_start - timedelta(minutes=1)
    window_end = minute_start + timedelta(minutes=1)

    qs = Habit.objects.filter(is_pleasant=False).exclude(last_reminded_at=today)
    sent = 0

    for h in qs.select_related("user"):
        # Проверка периодичности: раз в N дней от created_at
        days_passed = (today - h.created_at).days
        if days_passed % h.periodicity != 0:
            continue

        # Время привычки на сегодня (aware)
        scheduled_dt = timezone.make_aware(
            timezone.datetime.combine(today, h.time),
            timezone.get_current_timezone(),
        )

        # Попадаем ли в окно
        if not (window_start <= scheduled_dt < window_end):
            continue

        # Есть ли chat_id у пользователя
        tg = getattr(h.user, "telegram", None)
        chat_id = getattr(tg, "chat_id", None)
        if not chat_id:
            continue

        # Пытаемся отправить
        ok = send_telegram_message(chat_id, f"Напоминание: {h.action} в {h.place} — сейчас!")
        if ok:
            h.last_reminded_at = today
            h.save(update_fields=["last_reminded_at"])
            sent += 1

    return sent
