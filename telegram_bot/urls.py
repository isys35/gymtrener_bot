from telegram_bot.views import welcome, select_category

urls = [
    (r'<wc:req>/start', welcome),
    (r'/выбрать упражнение', select_category)
    ]