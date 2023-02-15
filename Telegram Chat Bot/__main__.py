# Телеграм чат-бот Пайтон старт
# Версия 0.3
# Чатбот переработан. Добвлена модульная система обновления функционала.

import time
import telebot


# конфигурация
from config import *
bot = telebot.TeleBot(TOKEN)
# Создаём переменные объекта, список для хранения всех известных пользователей
bot.all_users = []  # list(str)
# Словарь с коммандами будем храрить в объекте bot
bot.commands = {
    'start': 'Начать с начала',
    'help': 'Вывести помощь',
}

# вывод информации в консоль
import console
console.register_listener(bot)

# работа с пользователями
from users import *

# переменная для скрытия клавиатуры
from telebot import types
hide_keyoard = types.ReplyKeyboardRemove()


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m):
    cid = m.chat.id
    if cid not in Botuser.get_all_id() :   # Если пользователь ещё не известен:
        Botuser(cid).append_user()         # Создаём нового пользователя, его объект будет храниться в классе
        bot.send_message(cid, f"Здравия желаю, {m.from_user.first_name}! Приятно познакомиться.\n"+
                                'Я телебот написанный на пайтон.',
                                reply_markup=hide_keyoard)
        command_help(m)         # Показать справку
    else:
        botuser(cid).reset_mode()
        bot.send_message(cid, "Здравия желаю! Мы уже знакомы.", reply_markup=hide_keyoard)


# Функция, обрабатывающая команду /help
@bot.message_handler(commands=["help"])
def command_help(m):
    cid = m.chat.id
    help_text = "Вот что я умею:\n"
    for key in bot.commands:  # сгенерировать строку с командами из словаря commands, обозначеного в начале
        help_text += "/" + key + ": " + bot.commands[key] + "\n"
    bot.send_message(cid, help_text, reply_markup=hide_keyoard)


# Обработка всех остальных сообщений без режима
@bot.message_handler(content_types=["text"], 
                    func=lambda m: not m.text.startswith('/') and not botuser(m.chat.id).get_mode())
def no_mode_answer(m):
    cid = m.chat.id
    bot.send_message(cid, 'Прежде чем начать, нужно выбрать режим:')
    command_help(m)


# Подгружаем режимы работы бота
# import modules.talk as talk
# talk.initialize(bot, commands, user_mode)

import modules.online_trener as online_trener
# Если все переменные хранит объект bot, то кроме него нам ничего передавать не нужно
online_trener.initialize(bot)

# Посмотреть зарегистрированные функции
# for f in bot.message_handlers:
#     print(f)

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)