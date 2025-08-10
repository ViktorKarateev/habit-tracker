from django.utils import timezone
from celery import shared_task

from habits.models import Habit
from notifications.utils import send_telegram_message


@shared_task
def send_due_habits():
    """
    Раз в минуту:
    - берём локальное время
    - выбираем привычки, у которых совпало время (часы+минуты)
    - проверяем периодичность от created_at (каждые N дней)
    - не шлём повтор в тот же день (last_reminded_at)
    - если у пользователя есть telegram.chat_id — отправляем сообщение
    """
    now = timezone.localtime()
    today = now.date()
    hhmm = now.strftime("%H:%M")

    # Кандидаты по времени (приятные привычки — это награда, их не напоминаем как действие)
    candidates = Habit.objects.filter(  # type: ignore[attr-defined]
        time__hour=now.hour,
        time__minute=now.minute,
        is_pleasant=False,
    )

    for habit in candidates:
        # каждые N дней от даты создания
        days_since = (today - habit.created_at).days
        if days_since < 0 or days_since % habit.periodicity != 0:
            continue

        # уже напоминали сегодня
        if habit.last_reminded_at == today:
            continue

        # безопасно достанем chat_id
        telegram = getattr(habit.user, "telegram", None)
        chat_id = getattr(telegram, "chat_id", None)
        if not chat_id:
            continue

        reward_part = f"\nНаграда: {habit.reward}" if habit.reward else ""
        linked_part = (
            f"\nПосле — приятная привычка: {habit.linked_habit.action}"
            if habit.linked_habit else ""
        )
        text = (
            f"Напоминание по привычке:\n"
            f"Действие: {habit.action}\n"
            f"Место: {habit.place}\n"
            f"Время: {hhmm}{reward_part}{linked_part}"
        )

        if send_telegram_message(chat_id, text):
            habit.last_reminded_at = today
            habit.save(update_fields=["last_reminded_at"])
