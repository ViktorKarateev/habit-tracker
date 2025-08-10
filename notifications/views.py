from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema   # ← добавили
from .models import TelegramAccount
from .serializers import TelegramAccountSerializer


class SetChatIdView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(                      # ← это покажет body в Swagger
        request_body=TelegramAccountSerializer,
        responses={200: "chat_id сохранён"}
    )
    def post(self, request):
        serializer = TelegramAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chat_id = serializer.validated_data["chat_id"]
        TelegramAccount.objects.update_or_create(
            user=request.user, defaults={"chat_id": chat_id}
        )
        return Response({"detail": "chat_id сохранён"}, status=status.HTTP_200_OK)
