import json

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from telegram_bot.bot import Bot
from telegram_bot.core.telegram_context import TelegramContext
from telegram_bot.router import Router
from telegram_bot.urls import urls
from webhook.serializers import UpdateSerializer
from webhook.utils import save_json


class WebHook(APIView):
    """
    Вебхук для телеграмма
    """
    serializer_class = UpdateSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        save_json(request.body)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not serializer.data.get('message') and not serializer.data.get('callback_query'):
            return Response({"success": False, 'error':'Not message' }, status=status.HTTP_400_BAD_REQUEST)
        telegram_context = TelegramContext(settings.TELEGRAM_TOKEN)
        bot = Bot(telegram_context, serializer)
        router = Router(urls)
        router.url_dispatcher(bot)
        return Response({"success": True}, status=status.HTTP_200_OK)
