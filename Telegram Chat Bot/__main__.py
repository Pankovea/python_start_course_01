# Телеграм чат-бот Пайтон старт
# Версия 0.3
# Чатбот переработан. Добвлена модульная система обновления функционала.

import time
import telebot


# конфигурация
from config import *
bot = telebot.TeleBot(TOKEN)

# вывод информации в консоль
import console
console.register_listener(bot)

# работа с пользователями
from users import *

# переменная для скрытия клавиатуры
from telebot import types
hide_keyoard = types.ReplyKeyboardRemove()

# Словарь команд бота (основа)
commands = {
    'start': 'Начать с начала',
    'help': 'Вывести помощь',
}


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m):
    cid = m.chat.id
    if cid not in users:   # Если пользователь ещё не известен:
        users.append(cid)  # Сохраним его user id
        bot.send_message(cid, f"Здравия желаю, {m.from_user.first_name}! Приятно познакомиться.\n"+
                                'Я телебот написанный на пайтон. Меня научил общаться студент курса Пайтон старт Евгений, за что уему огромное спасибо.',
                                reply_markup=hide_keyoard)
        command_help(m)         # Показать справку
    else:
        reset_mode(cid)
        bot.send_message(cid, "Здравия желаю! Мы уже знакомы.", reply_markup=hide_keyoard)


# Функция, обрабатывающая команду /help
@bot.message_handler(commands=["help"])
def command_help(m):
    cid = m.chat.id
    help_text = "Вот что я умею:\n"
    for key in commands:  # сгенерировать строку с командами из словаря commands, обозначеного в начале
        help_text += "/" + key + ": " + commands[key] + "\n"
    bot.send_message(cid, help_text, reply_markup=hide_keyoard)


# Обработка всех остальных сообщений без режима
@bot.message_handler(content_types=["text"], 
                    func=lambda m: not m.text.startswith('/') and get_user_mode(m.chat.id) is None)
def no_mode_answer(m):
    cid = m.chat.id
    bot.send_message(cid, 'Прежде чем начать, нужно выбрать режим:')
    command_help(m)


# Подгружаем режимы работы бота
import modules.talk as talk
talk.initialize(bot, commands, user_mode)
import modules.online_trener as online_trener
online_trener.initialize(bot, commands, user_mode)
# Посмотреть зарегистрированные функции
for f in bot.message_handlers:
    print(f)

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)