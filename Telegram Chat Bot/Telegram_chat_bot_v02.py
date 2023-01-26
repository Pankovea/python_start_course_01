# 
# Учи Дома. Патон Старт
# Телеграм чат-бот версия 0.2
# 

import datetime
import time

import telebot
from telebot import types



# Создаем экземпляр бота
bot = telebot.TeleBot('5891059009:AAE2FYUXtn_7CRcFGFVd4Nu8nHqo14Zf5eU')

# 
# Объявляем глобальные переменные
# 
dialogs = {
    'Книги': [
        'Давай поговорим о книгах. Моё любимое произведение - пьеса А.Н.Островского "Банкрот". А какая твоя любимая книга?',
        'Интересно! Я никогда не читал "%answer", но в свободное время обязательно прочитаю! \nНа сегодня актуальны произведения из разряда фантастики. Советую прочитать книгу "451 градус по Фаренгейту" Роман, Рэй Брэдбери',
        'Давай до свиданья'
    ],
    'Музыка': [
        'Давай поговорим о музыке. Мне нравится классика, а что предпочитаешь слушать ты?',
        '"%answer" - это какой-то новый сингл? Обязательно послушаю!',
    ],
    'Увлечения': [
        'Я очень люблю общение, а мое любимое увлечение - игра с цифрами. Какое у тебя любимое занятие?',
        'Интересное занятие, "%answer". Главное, чтобы оно тебе нравилось)',
    ],
}

games = [
    'Угадай число',
]

ex = {
    '2 + 2':    '4',
    '10 / 2':   '5',
    '123 + 321': '444',
    '150 / 3': '50',
}

# 
# 
#   Функции режимов
# 
# 

def talk(m):
    cid = m.chat.id
    msgs = dialogs[user_theme[cid]] # список сообщений на тему
    user_answer = m.text if not (m.text.startswith('/') or m.text in dialogs.keys()) else ''
    if user_step[cid] != len(msgs):
        reply = msgs[user_step[cid]].replace('%answer', user_answer)
        bot.send_message(cid, reply, reply_markup=hide_keyoard)
        user_step[cid] += 1
    if user_step[cid] == len(msgs):
        bot.send_message(cid, 'На этом я исчерпан. Если хочешь, давай продолжим в другом режиме:')
        command_help(m)
        reset_mode(cid)
    else:
        bot.register_next_step_handler_by_chat_id(cid, talk)


def game(m):
    cid = m.chat.id
    bot.send_message(cid, 'Этот режим находится в разработке\nВыбери другой режим')

def ex(m):
    cid = m.chat.id
    bot.send_message(cid, 'Этот режим находится в разработке\nВыбери другой режим')


# 
# Объявляем глобальные переменные
# 

users = []  # Список 
user_mode = {}
user_theme = {}
user_step = {}

# Словарь команд бота
commands = {
    'start': 'Начать с начала',
    'help': 'Вывести помощь',
    'talk': 'Начать общаться',
    'game': 'Играть (в разработке)',
    'ex': 'Решать задачи (в разработке)'
}

# 
# Создадим клавиатуры для выбора поддтем
# 

theme_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
for k in dialogs.keys():    theme_keyboard.add(k)

game_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
for v in games:    game_keyboard.add(v)

# Скрыть клавиатуру
hide_keyoard = types.ReplyKeyboardRemove()

# 
# 
#   Вспомогательные фунции
# 
# 

def reset_mode(cid):
    user_mode.pop(cid, None)
    user_theme.pop(cid, None)
    user_step.pop(cid, None)

# Функция для вывода диалога в консоль
def listener(messages):
    """
    Когда приходят новые сообщения, они будут выводиться в консоль
    """
    for m in messages:
        if m.content_type == 'text':
            # вывести присланноое сообщение в консоль
            print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"), str(m.chat.first_name), "[" + str(m.chat.id) + "]: " + m.text)

bot.set_update_listener(listener)  # зарегистрировать вывод сообщений


# 
# 
#   Функции реакции на сообщения пользователя
# 
# 


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    cid = m.chat.id
    if cid not in users:   # Если пользователь ещё не известен:
        users.append(cid)  # Сохраним его user id
        bot.send_message(cid, f"Здравия желаю, {m.from_user.first_name}! Приятно познакомиться.\n"+
                                'Я телебот написанный на пайтон. Меня научил общаться студент курса Пайтон старт Евгений, за что уему огромное спасибо.',
                                reply_markup=hide_keyoard)
        command_help(m)         # Показать справку
    else:
        bot.send_message(cid, "Здравия желаю! Мы уже знакомы.", reply_markup=hide_keyoard)


# Функция, обрабатывающая команду /help
@bot.message_handler(commands=["help"])
def command_help(m, res=False):
    cid = m.chat.id
    help_text = "Вот что я умею:\n"
    for key in commands:  # сгенерировать строку с командами из словаря commands, обозначеного в начале
        help_text += "/" + key + ": " + commands[key] + "\n"
    bot.send_message(cid, help_text, reply_markup=hide_keyoard)


# Функция, обрабатывающая команду /talk
@bot.message_handler(commands=['talk'])
def start(m, res=False):
    cid = m.chat.id
    user_mode[cid] = 'talk'
    user_step[cid] = 0
    msg = 'Хорошо, давай пообщаемся. Что тебя интересует:\n'
    for k in dialogs.keys():
        msg += k + '\n'
    bot.send_message(cid, msg, reply_markup=theme_keyboard)

# Функция, обрабатывающая команду /game
@bot.message_handler(commands=["game"])
def start(m, res=False):
    cid = m.chat.id
    user_mode[cid] = 'game'
    user_step[cid] = 0
    msg = 'Хорошо. В какую игру ты хочешь поиграть:\n'
    for v in games:
        msg += v + '\n'
    bot.send_message(cid, msg, reply_markup=game_keyboard)

# Функция, обрабатывающая команду /ex
@bot.message_handler(commands=["ex"])
def start(m, res=False):
    cid = m.chat.id
    user_mode[cid] = 'ex'
    user_step[cid] = 0
    ex(m)

# Обработка первого сообщения в режиме или предложение войти в режим
@bot.message_handler(content_types=["text"])
def no_mode_answer(m):
    cid = m.chat.id
    # Если включен режим
    if user_mode.get(cid, 0) != 0:
        if user_mode[cid] == 'talk' and m.text in dialogs.keys():
            user_theme[cid] = m.text
            talk(m)
        elif user_mode[cid] == 'game' and m.text in games:
            user_theme[cid] = m.text
            game(m)
        elif user_mode[cid] == 'ex':
            user_theme[cid] = m.text
            ex(m)
        else:
            bot.send_message(cid, 'Такого мы ещё не проходили.')
    else:
        bot.send_message(cid, 'Извини, я не знаю о чем это. Выдери что-нибудь из:')
        command_help(m)


# 
# 
#   Запуск бота
# 
# 
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)