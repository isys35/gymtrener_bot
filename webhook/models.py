from django.db import models


class TelegramUser(models.Model):
    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, db_index=True, blank=True, default=None)
    username = models.CharField(max_length=100, db_index=True, default=None)


class TelegramMessage(models.Model):
    message_id = models.IntegerField()
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True, default=None)


class ChatSerializer(models.Model):
    type = models.CharField(max_length=50, db_index=True)
