from telegram_bot.views import welcome, select_category, select_exercise, previos_page_exercis, next_page_exercise, \
    exercise_info, exercise_use, close_exercise

urls = [
    (r'<wc:req>/start', welcome),
    (r'<wc:req>/главное меню', welcome),
    (r'/выбрать упражнение', select_category),
    (r'/выбрать упражнение/<str:category>', select_exercise),
    (r'/выбрать упражнение/<str:category>/<str:page_number>/назад', select_category),
    (r'/выбрать упражнение/<str:category>/<str:page_number>/следующая страница', next_page_exercise),
    (r'/выбрать упражнение/<str:category>/<str:page_number>/предыдущая страница', previos_page_exercis),
    (r'/выбрать упражнение/<str:category>/<str:page_number>/<str:exercise_id>', exercise_info),
    (r'/выбрать упражнение/<str:category>/<str:page_number>/<str:exercise_id>/назад', select_exercise),
    (r'/выбрать упражнение/<str:category>/<str:page_number>/<str:exercise_id>/выполнить упражнение', exercise_use),
    (r'/выбрать упражнение/<str:category>/<str:page_number>/<str:exercise_id>/выполнить упражнение/<str:exercise_use_id>/закончить упражнение', close_exercise),
    # (r'/выбрать упражнение/<str:category>/', exercise_info)
    ]