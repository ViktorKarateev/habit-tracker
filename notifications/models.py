from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TelegramAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='telegram')
    chat_id = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.user} -> {self.chat_id}"
