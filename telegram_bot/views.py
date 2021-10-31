from datetime import datetime

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count
from django.template.loader import render_to_string

from telegram_bot.bot import save_state, Bot
from webhook.models import Category, Exersice, ExerciseUse, Set, FavoritedExercises


@save_state("/")
def welcome(bot: Bot, **kwargs):
    message = render_to_string('welcome.html')
    bot.send_message(message, bot.keyboard.main())


def select_category(bot: Bot, **kwargs):
    categories = Category.objects.all()
    if not categories:
        bot.send_message("В базе нету упражнений 😔", bot.keyboard.main())
        bot.user.save_state('/')
        return
    bot.send_message("Выберите категорию упражнений", bot.keyboard.categories(categories))
    bot.user.save_state("/выбрать упражнение")


def select_exercise(bot: Bot, category: str, page_number=None, **kwargs):
    if page_number is None:
        page = 1
    else:
        page = int(page_number)
    exersices = Exersice.objects.filter(category__title=category).order_by('id')
    if not exersices:
        bot.send_message("В базе нету упражнений 😔", bot.keyboard.main())
        bot.user.save_state("/выбрать упражнение")
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
    try:
        exercise_id = int(exercise_id)
    except ValueError:
        bot.send_message('Неверно введён индекс упражнения 😧')
        return
    exercise = Exersice.objects.get(id=exercise_id)
    favorited_exrcise = FavoritedExercises.objects.filter(user_id=bot.user.id, exercise_id=exercise_id)
    exercise_uses = ExerciseUse.objects.filter(
        user_id=bot.user.id, exercise_id=exercise_id
    ).annotate(
        count_sets=Count('sets')
    ).exclude(
        count_sets=0
    ).order_by('date_start').prefetch_related('sets')
    last_exercise_use = exercise_uses.last()
    count_exercise_use = exercise_uses.count()
    sets = None
    if last_exercise_use:
        sets = last_exercise_use.sets.all()
    is_favorite = False
    if favorited_exrcise:
        is_favorite = True
    context = {'exercise': exercise,
               'favorite': is_favorite,
               'count_exercise_use': count_exercise_use,
               'last_exercise_use': last_exercise_use,
               'sets': sets}
    message = render_to_string('exercise.html', context=context)
    if exercise.image:
        message = bot.send_photo(message, exercise.image.file, bot.keyboard.exercise(is_favorite))
    else:
        message = bot.send_message(message, bot.keyboard.exercise(is_favorite))
    bot.user.save_state(f'/выбрать упражнение/{category}/{page_number}/{exercise_id}/{message.id}')


def exercise_use(bot: Bot, **kwargs):
    # TODO: Добавить логику в случае если нету упражнений в базе!
    exercise_use_id = kwargs.get('exercise_use_id')
    exercise_id = kwargs.get('exercise_id')
    if not exercise_use_id:
        exercise_use_obj = ExerciseUse.objects.create(exercise_id=int(exercise_id), user_id=bot.user.id)
        exercise_set = Set.objects.create(exercise_use=exercise_use_obj)
    else:
        exercise_use_obj = ExerciseUse.objects.get(id=int(exercise_use_id))
        last_exercise_set = exercise_use_obj.sets.all().order_by('-count_index').first()
        exercise_set = Set.objects.create(exercise_use=exercise_use_obj,
                                          count_index=last_exercise_set.count_index+1)
    context = {'set_count': exercise_set.count_index}
    message = render_to_string('exercise_use.html', context=context)
    bot.send_message(message, bot.keyboard.exercise_use())
    bot.user.save_state(f'/exercise_use/{exercise_id}/{exercise_use_obj.id}')


@save_state("/")
def close_exercise(bot: Bot, exercise_id: str, exercise_use_id: str):
    exercise_use_obj = ExerciseUse.objects.get(id=int(exercise_use_id))
    exercise_use_obj.date_finish = datetime.now()
    exercise_use_obj.save()
    text = 'Вы завершили упражнение, вот статистика бла бла бла'
    bot.send_message(text, bot.keyboard.main())


def input_mass(bot: Bot, exercise_id: str, exercise_use_id: str):
    text = 'Введите массу'
    bot.send_message(text, bot.keyboard.clear_keyboard())
    bot.user.save_state()


def input_repeat(bot: Bot, exercise_id: str, exercise_use_id: str, mass: str):
    # TODO: Написать валидатор
    try:
        mass = int(mass)
    except ValueError:
        bot.send_message('Неверна введена масса 😧, попробуйте ещё раз ')
        return
    text = 'Введите кол-во повторений'
    bot.send_message(text, bot.keyboard.clear_keyboard())
    bot.user.save_state()


def save_set(bot: Bot, exercise_id: str, exercise_use_id: str, mass: str, repeat: str):
    try:
        repeat = int(repeat)
    except ValueError:
        bot.send_message('Неверна введено кол-во повторений 😧, попробуйте ещё раз ')
        return
    exercise_use_obj = ExerciseUse.objects.get(id=int(exercise_use_id))
    last_set = exercise_use_obj.sets.all().order_by('-count_index').first()
    last_set.mass = int(mass)
    last_set.repeat = int(repeat)
    last_set.save()
    exercise_use(bot, exercise_id=exercise_id, exercise_use_id=exercise_use_id)


def favorite_action(bot: Bot, **kwargs):
    exercise_id = int(kwargs.get('exercise_id'))
    favorited = FavoritedExercises.objects.filter(user_id=bot.user.id, exercise_id=exercise_id)
    exercise = Exersice.objects.filter(id=exercise_id).first()
    message_id = kwargs.get('message_id')
    category = kwargs.get('category')
    page_number = kwargs.get('page_number')
    if not favorited:
        FavoritedExercises.objects.create(user_id=bot.user.id, exercise_id=exercise_id)
        context = {'exercise': exercise, 'favorite': True}
        keyboard = bot.keyboard.exercise(True)
    else:
        favorited.first().delete()
        context = {'exercise': exercise, 'favorite': False}
        keyboard = bot.keyboard.exercise(False)
    message_text = render_to_string('exercise.html', context=context)
    if exercise.image:
        message = bot.edit_message(message_text, message_id, keyboard, exercise.image.file)
    else:
        message = bot.edit_message(message_text, message_id, keyboard)
    bot.user.save_state(f'/выбрать упражнение/{category}/{page_number}/{exercise_id}/{message.id}')
