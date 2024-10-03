import os
import django
import requests
import telebot
from telebot import types
from desctop.core.models import Chat, Courses, TelegramAdmin

API_URL = 'http://localhost:8000/api/'
TELEGRAM_TOKEN = 'your_telegram_token'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desctop.settings')
django.setup()

bot = telebot.TeleBot(TELEGRAM_TOKEN)


def check_admin_privileges(telegram_id):
    """Проверка прав администратора через API"""
    response = requests.get(f"{API_URL}admins/{telegram_id}/")
    if response.status_code == 200:
        data = response.json()
        return data.get('is_confirmed', False)
    return False


@bot.message_handler(commands=['start'])
def start(message):
    """Обработка команды /start"""
    telegram_id = message.from_user.id
    if check_admin_privileges(telegram_id):
        bot.send_message(message.chat.id, "Добро пожаловать, администратор!")
        show_admin_panel(message.chat.id)
    else:
        bot.send_message(message.chat.id, "У вас нет прав администратора.")


def show_admin_panel(chat_id):
    """Показ панели администратора"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Рассылка"), types.KeyboardButton("Настройки"))
    bot.send_message(chat_id, "Панель администратора активирована.", reply_markup=markup)


def show_admin_panel(chat_id):
    """Показать панель администратора с выбором рассылки"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Рассылка в личные чаты"), types.KeyboardButton("Рассылка в группы"))
    markup.add(types.KeyboardButton("Курсы: Russian"), types.KeyboardButton("Курсы: O'zbek"))
    bot.send_message(chat_id, "Выберите тип рассылки:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_broadcast_choice(message):
    """Обработка выбора администратора для рассылки"""
    if message.text == "Рассылка в личные чаты":
        bot.send_message(message.chat.id, "Введите текст для рассылки:")
        bot.register_next_step_handler(message, send_personal_broad)
    elif message.text == "Рассылка в группы":
        bot.send_message(message.chat.id, "Введите текст для рассылки в группы:")
        bot.register_next_step_handler(message, send_group_broad)
    elif message.text == "Курсы: Russian":
        bot.send_message(message.chat.id, "Введите текст для рассылки по курсу 'Russian':")
        bot.register_next_step_handler(message, send_russian_course_broad)
    elif message.text == "Курсы: O'zbek":
        bot.send_message(message.chat.id, "Введите текст для рассылки по курсу 'O'zbek':")
        bot.register_next_step_handler(message, send_uzbek_course_broad)


def send_broadcast_message(message_text, target_course=None, target_type=None):
    """Отправка сообщения в зависимости от курса или типа чатов (группа или личный чат)"""
    if target_course:
        chats = Chat.objects.filter(course__name=target_course)
    elif target_type:
        chats = Chat.objects.filter(chat_type=target_type)
    else:
        chats = Chat.objects.all()

    for chat in chats:
        try:
            bot.send_message(chat.telegram_id, message_text)
            print(f"Сообщение отправлено в чат {chat.telegram_id}")
        except Exception as e:
            print(f"Ошибка отправки сообщения в чат {chat.telegram_id}: {e}")


def send_personal_broad(message):
    """Отправка рассылки в личные чаты"""
    send_broadcast_message(message.text, target_type='private')
    bot.send_message(message.chat.id, "Сообщение отправлено в личные чаты.")


def send_group_broad(message):
    """Отправка рассылки в группы"""
    send_broadcast_message(message.text, target_type='group')
    bot.send_message(message.chat.id, "Сообщение отправлено в группы.")


def send_russian_course_broad(message):
    """Отправка рассылки по курсу 'Russian'"""
    send_broadcast_message(message.text, target_course='Russian')
    bot.send_message(message.chat.id, "Сообщение отправлено на курс 'Russian'.")


def send_uzbek_course_broad(message):
    """Отправка рассылки по курсу 'O'zbek'"""
    send_broadcast_message(message.text, target_course='O\'zbek')
    bot.send_message(message.chat.id, "Сообщение отправлено на курс 'O'zbek'.")


if __name__ == '__main__':
    bot.polling(none_stop=True)
