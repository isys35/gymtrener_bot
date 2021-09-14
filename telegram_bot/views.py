from django.conf import settings
from django.core.paginator import Paginator
from django.template.loader import render_to_string

from telegram_bot.bot import save_state, Bot
from webhook.models import Category, Exersice, ExerciseUse, Set


@save_state("/")
def welcome(bot: Bot, **kwargs):
    message = render_to_string('welcome.html')
    bot.send_message(message, bot.keyboard.main())


@save_state("/выбрать упражнение")
def select_category(bot: Bot, **kwargs):
    categories = Category.objects.all()
    if not categories:
        bot.send_message("В базе нету упражнений 😔", bot.keyboard.main())
        return
    bot.send_message("Выберите категорию упражнений", bot.keyboard.categories(categories))


def select_exercise(bot: Bot, category: str, page_number=None, **kwargs):
    if page_number is None:
        page = 1
    else:
        page = int(page_number)
    exersices = Exersice.objects.filter(category__title=category).order_by('id')
    if not exersices:
        bot.send_message("В базе нету упражнений 😔", bot.keyboard.main())
        return
    paginator = Paginator(exersices, settings.PAGINATOR_SIZE)
    context = {'exersices': paginator.page(page)}
    message = render_to_string('exercises.html', context=context)
    bot.send_message(message, bot.keyboard.exercises(paginator.page(page)))
    bot.user.save_state(f'/выбрать упражнение/{category}/{page}')


def next_page_exercise(bot: Bot, category: str, page_number):
    page = int(page_number) + 1
    select_exercise(bot, category, page)


def previos_page_exercis(bot: Bot, category: str, page_number):
    page = int(page_number) - 1
    select_exercise(bot, category, page)


def exercise_info(bot: Bot, category: str, page_number: str, exercise_id: str):
    exercise = Exersice.objects.get(id=int(exercise_id))
    context = {'exercise': exercise}
    message = render_to_string('exercise.html', context=context)
    bot.send_message(message, bot.keyboard.exercise())
    bot.user.save_state()


def exercise_use(bot: Bot, category: str, page_number: str, exercise_id: str, exercise_use_id=None):
    if not exercise_use_id:
        exercise_use = ExerciseUse.objects.create(exercise_id=int(exercise_id), user_id=bot.user.id)
        exercise_set = Set.objects.create(exercise_use=exercise_use)
    else:
        pass
    context = {'set_count': exercise_set.count_index}
    message = render_to_string('exercise_use.html', context=context)
    bot.send_message(message, bot.keyboard.exercise_use())