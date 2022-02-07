from typing import Union

from django.db import models
from django.db.models import CharField, IntegerField, ForeignKey, ManyToManyField, DateTimeField, TextField


class TelegramUser(models.Model):
    first_name: CharField = CharField(max_length=100, db_index=True)
    last_name: CharField = CharField(max_length=100, db_index=True, blank=True, null=True, default=None)
    username: CharField = CharField(max_length=100, db_index=True, default=None)
    state: ForeignKey = ForeignKey('State', on_delete=models.SET_NULL, blank=True, null=True,
                                   default=None)
    favorite_exercises: ManyToManyField = models.ManyToManyField('Exersice', through='FavoritedExercises')


class TelegramMessage(models.Model):
    message_id: IntegerField = IntegerField()
    user: ForeignKey = ForeignKey(TelegramUser, on_delete=models.CASCADE)
    date: DateTimeField = DateTimeField(auto_now_add=True)
    text: TextField = TextField(blank=True, default=None)


class FavoritedExercises(models.Model):
    class Meta:
        unique_together = ("user", "exercise")

    user: ForeignKey = ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
    )
    exercise: ForeignKey = ForeignKey(
        'Exersice',
        on_delete=models.CASCADE,
    )


class ChatSerializer(models.Model):
    type: CharField = CharField(max_length=50, db_index=True)


class Category(models.Model):
    title: CharField = CharField(max_length=100, db_index=True, unique=True)

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Exersice(models.Model):
    title: CharField = CharField(max_length=100, db_index=True, unique=True)
    category: ForeignKey = ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    description: TextField = TextField(blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.title}"


class ExerciseUse(models.Model):
    exercise: ForeignKey = ForeignKey(Exersice, on_delete=models.CASCADE)
    user: ForeignKey = ForeignKey(TelegramUser, on_delete=models.CASCADE)
    date_start: DateTimeField = DateTimeField(auto_now_add=True, blank=True, null=True)
    date_finish: DateTimeField = DateTimeField(blank=True, null=True, default=None)


class Set(models.Model):
    exercise_use: ForeignKey = ForeignKey(ExerciseUse, on_delete=models.CASCADE, related_name='sets')
    count_index: IntegerField = IntegerField(default=1)
    repeat: IntegerField = IntegerField(default=0)
    mass: IntegerField = IntegerField(default=0)


class View(models.Model):
    text: Union[TextField, str] = TextField()
    function: Union[CharField, str] = CharField(max_length=250, blank=True, null=True)
    new_state: Union[ForeignKey, 'State'] = ForeignKey('State',
                                                       null=True,
                                                       blank=True,
                                                       on_delete=models.SET_NULL,
                                                       related_name='views_new')
    translate_state_to: Union[ForeignKey, 'State'] = ForeignKey('State',
                                                                null=True,
                                                                blank=True,
                                                                on_delete=models.SET_NULL,
                                                                related_name='views_traslated')
    keyboard: ForeignKey = ForeignKey('Keyboard',
                                      null=True,
                                      blank=True,
                                      related_name='views',
                                      on_delete=models.SET_NULL)

    def __str__(self):
        return self.text


class State(models.Model):
    parent: ForeignKey = ForeignKey('State', null=True, blank=True, on_delete=models.CASCADE)
    text: CharField = CharField(max_length=200, null=True, blank=True)
    button: ForeignKey = ForeignKey('ReplyButton', null=True, blank=True, on_delete=models.SET_NULL)
    name_parameter: CharField = CharField(max_length=200, null=True, blank=True)
    view: ForeignKey = ForeignKey(View, on_delete=models.CASCADE, related_name='states', null=True, blank=True)

    def __str__(self):
        return f"id:{self.id} text:{self.text} button:{self.button} name_parameter:{self.name_parameter}"


class StateParameter(models.Model):
    state: ForeignKey = ForeignKey('State', on_delete=models.CASCADE)
    value: CharField = CharField(max_length=200)
    user: ForeignKey = ForeignKey(TelegramUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['state', 'user']


class Keyboard(models.Model):
    pass


class ReplyButton(models.Model):
    keyboard: ForeignKey = ForeignKey(Keyboard, blank=True, null=True, on_delete=models.CASCADE,
                                      related_name='buttons')
    text: CharField = CharField(max_length=250)

    def __str__(self):
        return self.text
