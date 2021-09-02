from django.db import models


class TelegramUser(models.Model):
    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, db_index=True, blank=True, default=None)
    username = models.CharField(max_length=100, db_index=True, default=None)
    state = models.CharField(max_length=200, default='/')


class TelegramMessage(models.Model):
    message_id = models.IntegerField()
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True, default=None)


class ChatSerializer(models.Model):
    type = models.CharField(max_length=50, db_index=True)


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True, unique=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
