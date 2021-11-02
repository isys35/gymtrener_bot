from telegram_bot.views import welcome, select_category, select_exercise, previos_page_exercis, next_page_exercise, \
    exercise_info, exercise_use, close_exercise, input_mass, input_repeat, save_set, favorite_action, favorite_exercises

urls = [
    (r'<wc:req>/start', welcome),
    (r'<wc:req>/главное меню', welcome),
    (r'/выбрать упражнение', select_category),
    (r'/выбрать упражнение/<str:category>', select_exercise),
    (r'/выбрать упражнение/<str:category>/<str:page_number>/назад', select_category),
    (r'/выбрать упражнение/<str:category>/<str:page_number>/следующая страница', next_page_exercise),
    (r'/выбрать упражнение/<str:category>/<str:page_number>/предыдущая страница', previos_page_exercis),
    (r'/выбрать упражнение/<str:category>/<str:page_number>/<str:exercise_id>', exercise_info),
    (r'/выбрать упражнение/<str:category>/<str:page_number>/<str:exercise_id>/<str:message_id>/назад', select_exercise),
    (r'/выбрать упражнение/<str:category>/<str:page_number>/<str:exercise_id>/<str:message_id>/выполнить упражнение', exercise_use),
    (r'/выбрать упражнение/<str:category>/<str:page_number>/<str:exercise_id>/<str:message_id>/добавить в избранное', favorite_action),
    (r'/выбрать упражнение/<str:category>/<str:page_number>/<str:exercise_id>/<str:message_id>/удалить из избранного', favorite_action),

    (r'/exercise_use/<str:exercise_id>/<str:exercise_use_id>/закончить упражнение', close_exercise),
    (r'/exercise_use/<str:exercise_id>/<str:exercise_use_id>/продолжить', input_mass),
    (r'/exercise_use/<str:exercise_id>/<str:exercise_use_id>/продолжить/<str:mass>', input_repeat),
    (r'/exercise_use/<str:exercise_id>/<str:exercise_use_id>/продолжить/<str:mass>/<str:repeat>', save_set),

    (r'/избранные упражнения', favorite_exercises)
    # (r'/выбрать упражнение/<str:category>/', exercise_info)
    ]