from rest_framework import viewsets, permissions
from .models import Habit
from .serializers import HabitSerializer
from rest_framework import generics
from habit_tracker.pagination import HabitPagination

class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [permissions.AllowAny]

