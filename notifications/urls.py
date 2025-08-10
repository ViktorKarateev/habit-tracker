from django.urls import path
from .views import SetChatIdView

urlpatterns = [
    path("chat-id/", SetChatIdView.as_view(), name="set-chat-id"),
]
