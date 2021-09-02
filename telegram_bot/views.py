from telegram_bot.bot import save_state
from webhook.models import Category


@save_state("/")
def welcome(bot, **kwargs):
    text_message = "%ПРИВЕТСТВИЕ%"
    bot.send_message(text_message, bot.keyboard.main())


@save_state("/выбрать упражнение")
def select_category(bot):
    categories = Category.objects.all()
    bot.send_message("Выберите категорию упражнений", bot.keyboard.categories(categories))
