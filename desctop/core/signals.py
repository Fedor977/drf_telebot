import telebot.types
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TelegramAdmin
from telebot import TeleBot
from django.conf import settings

bot = TeleBot(settings.TELEGRAM_TOKEN)


@receiver(post_save, sender=TelegramAdmin)
def send_confirmation_message(sender, instance, created, **kwargs):
    """Уведомление, об успешном назначении адмиа"""
    if not instance.is_comfirmed:
        confirmation_text = (
            f'Здравствуйте, {instance.name}!'
            "Вас назначили админом"
        )

        markup = telebot.types.InlineKeyboardMarkup()
        confirm_button = telebot.types.InlineQueryResultsButton(text="Подтвердить", callback_data=f'confirm_{instance.telegram_id}')
        markup.add(confirm_button)

        try:
            bot.send_message(instance.telegram_id, confirmation_text, replay_markup=markup)
            print(f'Сообщение отправлено пользователю c именем {instance.telegram_id}')
        except Exception as e:
            print(f'Ошибка при отправке сообщения {e}')