from rest_framework import viewsets, permissions, generics
from .models import Habit
from .serializers import HabitSerializer
from habit_tracker.pagination import HabitPagination
from .permissions import IsOwnerOrReadOnly


class HabitViewSet(viewsets.ModelViewSet):
    """
    CRUD по привычкам текущего пользователя.
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = HabitSerializer
    pagination_class = HabitPagination

    def get_queryset(self):
        # Сортировка нужна, чтобы не ловить UnorderedObjectListWarning при пагинации
        return Habit.objects.filter(user=self.request.user).order_by("id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    """
    Публичные привычки (is_public=True) для общего доступа.
    """
    queryset = Habit.objects.filter(is_public=True).order_by("id")
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [permissions.AllowAny]
