from datetime import datetime

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count
from django.template.loader import render_to_string

from telegram_bot.bot import save_state, Bot
# from telegram_bot.views_dispatcher import ViewDispatcher
from webhook.models import Category, Exersice, ExerciseUse, Set, FavoritedExercises


# @save_state("/")
# def welcome(bot: Bot, **kwargs):
#     message = render_to_string('welcome.html')
#     bot.send_message(message, bot.keyboard.main())


def select_category(dispatcher):
    categories = Category.objects.all()
    dispatcher.bot.send_message(dispatcher.text, dispatcher.bot.keyboard.categories(categories))


# def select_exercise(bot: Bot, category: str, **kwargs):
#     page_number = kwargs.get('page_number') or 1
#     page_number = int(page_number)
#     exersices = Exersice.objects.filter(category__title=category).order_by('id')
#     if not exersices:
#         bot.send_message("В базе нету упражнений 😔", bot.keyboard.main())
#         bot.user.save_state("/выбрать упражнение")
#         return
#     paginator = Paginator(exersices, settings.PAGINATOR_SIZE)
#     context = {'exersices': paginator.page(page_number)}
#     message = render_to_string('exercises.html', context=context)
#     bot.send_message(message, bot.keyboard.exercises(paginator.page(page_number)))
#     bot.user.save_state(f'/выбрать упражнение/{category}/{page_number}')
#
#
# def next_page_exercise(bot: Bot, category: str, page_number):
#     page = int(page_number) + 1
#     select_exercise(bot, category, page_number=page)
#
#
# def previos_page_exercis(bot: Bot, category: str, page_number):
#     page = int(page_number) - 1
#     select_exercise(bot, category, page_number=page)
#
#
# def exercise_info(bot: Bot, **kwargs):
#     try:
#         exercise_id = int(kwargs.get('exercise_id'))
#     except ValueError:
#         bot.send_message('Неверно введён индекс упражнения 😧')
#         return
#     exercise = Exersice.objects.filter(id=exercise_id).select_related('category').first()
#     favorited_exrcise = FavoritedExercises.objects.filter(user_id=bot.user.id, exercise_id=exercise_id)
#     exercise_uses = ExerciseUse.objects.filter(
#         user_id=bot.user.id, exercise_id=exercise_id
#     ).annotate(
#         count_sets=Count('sets')
#     ).exclude(
#         count_sets=0
#     ).order_by('date_start').prefetch_related('sets')
#     last_exercise_use = exercise_uses.last()
#     count_exercise_use = exercise_uses.count()
#     sets = None
#     if last_exercise_use:
#         sets = last_exercise_use.sets.all()
#     is_favorite = False
#     if favorited_exrcise:
#         is_favorite = True
#     context = {'exercise': exercise,
#                'favorite': is_favorite,
#                'count_exercise_use': count_exercise_use,
#                'last_exercise_use': last_exercise_use,
#                'sets': sets}
#     message = render_to_string('exercise.html', context=context)
#     if exercise.image:
#         message = bot.send_photo(message, exercise.image.file, bot.keyboard.exercise(is_favorite))
#     else:
#         message = bot.send_message(message, bot.keyboard.exercise(is_favorite))
#     page_number = kwargs.get('page_number') or 1
#     bot.user.save_state(f'/выбрать упражнение/{exercise.category.title}/{page_number}/{exercise_id}/{message.id}')
#
#
# def exercise_use(bot: Bot, **kwargs):
#     # TODO: Добавить логику в случае если нету упражнений в базе!
#     exercise_use_id = kwargs.get('exercise_use_id')
#     exercise_id = kwargs.get('exercise_id')
#     if not exercise_use_id:
#         exercise_use_obj = ExerciseUse.objects.create(exercise_id=int(exercise_id), user_id=bot.user.id)
#         exercise_set = Set.objects.create(exercise_use=exercise_use_obj)
#     else:
#         exercise_use_obj = ExerciseUse.objects.get(id=int(exercise_use_id))
#         last_exercise_set = exercise_use_obj.sets.all().order_by('-count_index').first()
#         exercise_set = Set.objects.create(exercise_use=exercise_use_obj,
#                                           count_index=last_exercise_set.count_index + 1)
#     context = {'set_count': exercise_set.count_index}
#     message = render_to_string('exercise_use.html', context=context)
#     bot.send_message(message, bot.keyboard.exercise_use())
#     bot.user.save_state(f'/exercise_use/{exercise_id}/{exercise_use_obj.id}')
#
#
# @save_state("/")
# def close_exercise(bot: Bot, exercise_id: str, exercise_use_id: str):
#     exercise_use_obj = ExerciseUse.objects.filter(id=int(exercise_use_id)).prefetch_related('sets').first()
#     exercise_use_obj.date_finish = datetime.now()
#     exercise_use_obj.save()
#     sets = [_set for _set in exercise_use_obj.sets.all() if _set.repeat]
#     context = {'sets': sets, 'sets_count': len(sets)}
#     message = render_to_string('close_exercise.html', context=context)
#     bot.send_message(message, bot.keyboard.main())
#
#
# def input_mass(bot: Bot, exercise_id: str, exercise_use_id: str):
#     text = 'Введите массу утяжелителя'
#     bot.send_message(text, bot.keyboard.clear_keyboard())
#     bot.user.save_state()
#
#
# def input_repeat(bot: Bot, exercise_id: str, exercise_use_id: str, mass: str):
#     # TODO: Написать валидатор
#     try:
#         mass = int(mass)
#     except ValueError:
#         bot.send_message('Неверна введена масса 😧, попробуйте ещё раз ')
#         return
#     text = 'Введите кол-во повторений'
#     bot.send_message(text, bot.keyboard.clear_keyboard())
#     bot.user.save_state()
#
#
# def save_set(bot: Bot, exercise_id: str, exercise_use_id: str, mass: str, repeat: str):
#     try:
#         repeat = int(repeat)
#     except ValueError:
#         bot.send_message('Неверна введено кол-во повторений 😧, попробуйте ещё раз ')
#         return
#     exercise_use_obj = ExerciseUse.objects.get(id=int(exercise_use_id))
#     last_set = exercise_use_obj.sets.all().order_by('-count_index').first()
#     last_set.mass = int(mass)
#     last_set.repeat = int(repeat)
#     last_set.save()
#     exercise_use(bot, exercise_id=exercise_id, exercise_use_id=exercise_use_id)
#
#
# def favorite_action(bot: Bot, **kwargs):
#     exercise_id = int(kwargs.get('exercise_id'))
#     favorited = FavoritedExercises.objects.filter(user_id=bot.user.id, exercise_id=exercise_id)
#     exercise = Exersice.objects.filter(id=exercise_id).first()
#     message_id = kwargs.get('message_id')
#     category = kwargs.get('category')
#     page_number = kwargs.get('page_number')
#     if not favorited:
#         FavoritedExercises.objects.create(user_id=bot.user.id, exercise_id=exercise_id)
#         context = {'exercise': exercise, 'favorite': True}
#         keyboard = bot.keyboard.exercise(True)
#     else:
#         favorited.first().delete()
#         context = {'exercise': exercise, 'favorite': False}
#         keyboard = bot.keyboard.exercise(False)
#     message_text = render_to_string('exercise.html', context=context)
#     if exercise.image:
#         message = bot.edit_message(message_text, message_id, keyboard, exercise.image.file)
#     else:
#         message = bot.edit_message(message_text, message_id, keyboard)
#     bot.user.save_state(f'/выбрать упражнение/{category}/{page_number}/{exercise_id}/{message.id}')
#
#
# def favorite_exercises(bot: Bot, **kwargs):
#     user_id = bot.user.id
#     favorite_exercises = FavoritedExercises.objects.filter(user_id=user_id). \
#         select_related('exercise'). \
#         order_by('exercise_id'). \
#         all()
#     if not favorite_exercises:
#         bot.send_message('Избранные упражнения не найдены 😧', bot.keyboard.main())
#         bot.user.save_state('/')
#         return
#     page_number = kwargs.get('page_number') or 1
#     page_number = int(page_number)
#     paginator = Paginator(favorite_exercises, settings.PAGINATOR_SIZE)
#     exercises = [{'id': favorite_exercise.exercise.id, 'title': favorite_exercise.exercise.title}
#                  for favorite_exercise in paginator.page(page_number)]
#     context = {'exercises': exercises}
#     message_text = render_to_string('favorite_exercises.html', context=context)
#     bot.send_message(message_text, bot.keyboard.favorite_exercises(paginator.page(page_number)))
#     bot.user.save_state(f'/избранные упражнения/{page_number}')
#
#
# def last_exercises(bot: Bot, **kwargs):
#     user_id = bot.user.id
#     last_exerciseuses = ExerciseUse.objects \
#                             .filter(user_id=user_id) \
#                             .distinct('exercise_id') \
#                             .order_by('exercise_id', '-date_finish') \
#                             .select_related('exercise')[:10]
#     if not last_exerciseuses:
#         bot.send_message('Упражнения не найдены 😧', bot.keyboard.main())
#         bot.user.save_state('/')
#         return
#     exercises = [{'id': last_exerciseuse.exercise.id,
#                   'title': last_exerciseuse.exercise.title,
#                   'date': last_exerciseuse.date_finish}
#                  for last_exerciseuse in last_exerciseuses]
#     context = {'exercises': exercises}
#     message_text = render_to_string('last_exercises.html', context=context)
#     bot.send_message(message_text, bot.keyboard.last_exercises(exercises))
#     bot.user.save_state()
