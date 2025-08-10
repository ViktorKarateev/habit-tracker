from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError

User = get_user_model()


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits', verbose_name="Пользователь")
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    linked_habit = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'is_pleasant': True},
        related_name='linked_to',
        verbose_name="Связанная привычка"
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Создано")
    last_reminded_at = models.DateField(null=True, blank=True, verbose_name="Последнее напоминание")
    periodicity = models.PositiveSmallIntegerField(default=1, verbose_name="Периодичность (в днях)")
    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name="Вознаграждение")
    execution_time = models.PositiveSmallIntegerField(verbose_name="Время на выполнение (в секундах)")
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")

    def __str__(self):
        return f"{self.action} в {self.time} ({self.user})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"


    def clean(self):
        # Приятная привычка не может иметь связанной привычки или награды
        if self.is_pleasant and (self.reward or self.linked_habit):
            raise ValidationError("Приятная привычка не может иметь ни награды, ни связанной привычки.")

        # Поля reward и linked_habit — взаимоисключающие
        if self.reward and self.linked_habit:
            raise ValidationError("Нельзя одновременно указать и награду, и связанную привычку.")

        # Только приятные привычки могут быть связаны
        if self.linked_habit and not self.linked_habit.is_pleasant:
            raise ValidationError("Можно указать только приятную привычку в качестве связанной.")

        # Время выполнения не должно превышать 120 секунд
        if self.execution_time > 120:
            raise ValidationError("Время на выполнение не должно превышать 120 секунд.")

        # Периодичность не может быть больше 7 дней
        if self.periodicity > 7:
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)