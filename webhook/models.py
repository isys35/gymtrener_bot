from django.db import models


class TelegramUser(models.Model):
    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, db_index=True)
    username = models.CharField(max_length=100, db_index=True, unique=True)


class TelegramMessage(models.Model):
    message_id = models.IntegerField()
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    date = models.DateTimeField()
    text = models.TextField()


class ChatSerializer(models.Model):
    type = models.CharField(max_length=50, db_index=True)
