from django.db import models


class TelegramUser(models.Model):
    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, db_index=True, blank=True, null=True, default=None)
    username = models.CharField(max_length=100, db_index=True, default=None)
    state = models.ForeignKey('State', on_delete=models.SET_NULL, blank=True, null=True, default=None)
    favorite_exercises = models.ManyToManyField('Exersice', through='FavoritedExercises')


class TelegramMessage(models.Model):
    message_id = models.IntegerField()
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True, default=None)


class FavoritedExercises(models.Model):
    class Meta:
        unique_together = ("user", "exercise")

    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
    )
    exercise = models.ForeignKey(
        'Exersice',
        on_delete=models.CASCADE,
    )


class ChatSerializer(models.Model):
    type = models.CharField(max_length=50, db_index=True)


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True, unique=True)

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Exersice(models.Model):
    title = models.CharField(max_length=100, db_index=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True, null=True, default=None)
    image = models.ImageField(upload_to='images', blank=True)
    details_url = models.URLField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        self.details_url = 'https://www.google.com/search?q=' + self.title.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class ExerciseUse(models.Model):
    exercise = models.ForeignKey(Exersice, on_delete=models.CASCADE)
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    date_start = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_finish = models.DateTimeField(blank=True, null=True, default=None)


class Set(models.Model):
    exercise_use = models.ForeignKey(ExerciseUse, on_delete=models.CASCADE, related_name='sets')
    count_index = models.IntegerField(default=1)
    repeat = models.IntegerField(default=0)
    mass = models.IntegerField(default=0)


class View(models.Model):
    text = models.TextField()
    function = models.CharField(max_length=250, blank=True, null=True)
    new_state = models.ForeignKey('State', null=True, blank=True, on_delete=models.SET_NULL, related_name='views')
    keyboard = models.ForeignKey('Keyboard', null=True, blank=True, on_delete=models.SET_NULL, related_name='views')

    def __str__(self):
        return self.text


class State(models.Model):
    parent = models.ForeignKey('State', null=True, blank=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, null=True, blank=True)
    button = models.ForeignKey('ReplyButton', null=True, blank=True, on_delete=models.SET_NULL)
    name_parameter = models.CharField(max_length=200, null=True, blank=True)
    view = models.ForeignKey(View, on_delete=models.CASCADE, related_name='states', null=True, blank=True)

    def __str__(self):
        return self.text or self.button.text


class StateParameter(models.Model):
    state = models.ForeignKey('State', on_delete=models.CASCADE)
    value = models.CharField(max_length=200)
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['state', 'user']


class Keyboard(models.Model):
    pass


class ReplyButton(models.Model):
    keyboard = models.ForeignKey(Keyboard, blank=True, null=True, on_delete=models.CASCADE, related_name='buttons')
    text = models.CharField(max_length=250)

    def __str__(self):
        return self.text
