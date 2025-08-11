# habits/models.py
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

User = get_user_model()


class Habit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=255, verbose_name="Действие")

    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")

    linked_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={"is_pleasant": True},
        related_name="linked_to",
        verbose_name="Связанная привычка",
    )

    created_at = models.DateField(auto_now_add=True, verbose_name="Создано")
    last_reminded_at = models.DateField(
        null=True, blank=True, verbose_name="Последнее напоминание"
    )

    periodicity = models.PositiveSmallIntegerField(
        default=1,
        validators=[MaxValueValidator(7)],
        verbose_name="Периодичность (в днях)",
    )

    reward = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Вознаграждение"
    )

    execution_time = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(120)],
        verbose_name="Время на выполнение (в секундах)",
    )

    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")

    def __str__(self):
        return f"{self.action} в {self.time} ({self.user})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        # Чёткий порядок для пагинации/тестов
        ordering = ["-created_at", "id"]

    def clean(self):
        errors = {}

        # Приятная привычка не может иметь награду или ссылку
        if self.is_pleasant and self.reward:
            errors["reward"] = "Приятная привычка не может иметь награду."
        if self.is_pleasant and self.linked_habit:
            errors["linked_habit"] = "Приятная привычка не может иметь связанную привычку."

        # Нельзя одновременно указать награду и связанную привычку
        if self.reward and self.linked_habit:
            errors["linked_habit"] = "Нельзя одновременно указать и награду, и связанную привычку."

        # Связанная привычка должна быть приятной
        if self.linked_habit and not self.linked_habit.is_pleasant:
            errors["linked_habit"] = "Можно указать только приятную привычку в качестве связанной."

        # Для НЕприятной — должна быть награда или связанная приятная (если нужно жёстко)
        if not self.is_pleasant and not (self.reward or self.linked_habit):
            errors["reward"] = "Укажите награду или связанную приятную привычку."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
