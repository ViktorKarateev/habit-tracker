from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("id", "user", "created_at", "last_reminded_at")

    def validate_execution_time(self, v: int):
        # 1..120 секунд
        if v is None or v <= 0 or v > 120:
            raise serializers.ValidationError("Время выполнения должно быть от 1 до 120 секунд.")
        return v

    def validate_periodicity(self, v: int):
        # 1..7 дней
        if v is None or v < 1 or v > 7:
            raise serializers.ValidationError("Периодичность должна быть от 1 до 7 дней.")
        return v

    def validate(self, attrs):
        # поддержка PATCH: берём текущее значение из instance, если не пришло в attrs
        def get_val(name):
            return attrs.get(name, getattr(self.instance, name, None))

        is_pleasant = get_val("is_pleasant")
        reward = get_val("reward")
        linked = get_val("linked_habit")

        # Приятная привычка: без награды и без связанной
        if is_pleasant:
            if reward:
                raise serializers.ValidationError({"reward": "Для приятной привычки нельзя указывать вознаграждение."})
            if linked is not None:
                raise serializers.ValidationError({"linked_habit": "Приятную привычку нельзя связывать с другой."})

        # Обычная (неприятная): нужна либо награда, либо связанная приятная, но не оба сразу
        else:
            if not reward and not linked:
                raise serializers.ValidationError("Укажите вознаграждение или связанную приятную привычку.")
            if reward and linked:
                raise serializers.ValidationError("Нельзя одновременно указывать вознаграждение и связанную привычку.")
            if linked and not linked.is_pleasant:
                raise serializers.ValidationError({"linked_habit": "Связанная привычка должна быть приятной."})

            # Разрешим связывать только свои привычки (если нужно — можно убрать это правило)
            req = self.context.get("request")
            user = getattr(req, "user", None)
            if linked and user and linked.user != user:
                raise serializers.ValidationError({"linked_habit": "Можно связывать только свои привычки."})

        return attrs
