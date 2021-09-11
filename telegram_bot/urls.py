from telegram_bot.views import welcome, select_category, select_exercise, exercise_info

urls = [
    (r'<wc:req>/start', welcome),
    (r'/выбрать упражнение', select_category),
    (r'/выбрать упражнение/<str:category>', select_exercise),
    (r'/выбрать упражнение/<str:category>/callback', exercise_info)
    ]