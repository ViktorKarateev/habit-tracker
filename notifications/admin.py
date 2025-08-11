from django.contrib import admin
from .models import TelegramAccount


@admin.register(TelegramAccount)
class TelegramAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "chat_id", "created_at")
    search_fields = ("user__username", "chat_id")
