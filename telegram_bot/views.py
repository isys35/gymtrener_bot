from django.template.loader import render_to_string

from telegram_bot.bot import save_state, Bot
from webhook.models import Category, Exersice


@save_state("/")
def welcome(bot: Bot, **kwargs):
    message = render_to_string('welcome.html')
    bot.send_message(message, bot.keyboard.main())


@save_state("/выбрать упражнение")
def select_category(bot: Bot):
    categories = Category.objects.all()
    if not categories:
        bot.send_message("В базе нету упражнений 😔", bot.keyboard.main())
        return
    bot.send_message("Выберите категорию упражнений", bot.keyboard.categories(categories))


def select_exercise(bot: Bot, category: str):
    exersices = Exersice.objects.filter(category__title=category)
    if not exersices:
        bot.send_message("В базе нету упражнений 😔", bot.keyboard.main())
        return
    context = {'exersices': exersices}
    message = render_to_string('exercises.html', context=context)
    bot.send_message(message, bot.keyboard.exercises(exersices))
    bot.user.save_state(f'/выбрать упражнение/{category}')


def exercise_info(bot: Bot, **kwargs):
    exercise = Exersice.objects.get(id=bot.user.callback)
    context = {'exercise': exercise}
    message = render_to_string('exercise.html', context=context)
    bot.edit_message(message, bot.user.update_handler.get_message_id())
    bot.user.save_state()