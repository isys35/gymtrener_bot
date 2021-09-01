from telegram_bot.views import welcome

urls = [
    (r'<wc:req>/start', welcome),
    ]