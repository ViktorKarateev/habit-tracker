from django.contrib import admin
from .models import TelegramAccount


@admin.register(TelegramAccount)
class TelegramAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "chat_id")  # убрали created_at
    search_fields = ("user__username", "chat_id")
    list_select_related = ("user",)
