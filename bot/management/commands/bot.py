from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import TeleBot


from bot.models import User,Post


# Объявление переменной бота
bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


# Название класса обязательно - "Command"
class Command(BaseCommand):
  	# Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2) # Сохранение обработчиков
        bot.load_next_step_handlers()								# Загрузка обработчиков
        bot.infinity_polling()											# Бесконечный цикл бота



from telegram.ext import CommandHandler

def start(bot, update):
    # Получаем информацию о пользователе
    user = update.message.from_user
    telegram_id = user.id
    first_name = user.first_name
    last_name = user.last_name

    # Создаем пользователя в базе данных, если он еще не существует
    try:
        User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        User.objects.create(telegram_id=telegram_id, first_name=first_name, last_name=last_name)

    # Отправляем сообщение пользователю
    bot.send_message(chat_id=update.message.chat_id, text="Привет! Я бот созданный с помощью Django и pyTelegramBotAPI.")

start_handler = CommandHandler('start', start)


from telegram.ext import Updater

updater = Updater(token='YOUR_BOT_TOKEN')
dispatcher = updater.dispatcher

dispatcher.add_handler(start_handler)

updater.start_polling()
        