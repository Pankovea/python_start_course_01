# import telebot
from telebot import types

# Функция добавления режима
MODULE_COMMAND = 'talk'

def initialize(outer_bot, commands, outer_user_mode):
    global user_mode
    global bot
    user_mode = outer_user_mode
    bot = outer_bot
    commands[MODULE_COMMAND] = 'Начать общаться'
    bot.register_message_handler(callback=module_start_command, commands=[MODULE_COMMAND])
    bot.register_message_handler(callback=mode_answer, content_types=["text"], 
                                 func=lambda m: user_mode.get(m.chat.id, None) == MODULE_COMMAND)


# Объявляем переменные модуля
user_theme = {}
user_step = {}
# переменная с диалогами
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

# Создадим клавиатуры для выбора поддтем
theme_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
for k in dialogs.keys():
    theme_keyboard.add(k)
hide_keyoard = types.ReplyKeyboardRemove()


# Функция, обрабатывающая команду /MODULE_COMMAND
# @bot.message_handler(commands=[MODULE_COMMAND])
def module_start_command(m):
    cid = m.chat.id
    user_mode[cid] = 'talk'
    user_step[cid] = 0
    msg = 'Хорошо, давай пообщаемся. Что тебя интересует:\n'
    for k in dialogs.keys():
        msg += k + '\n'
    bot.send_message(cid, msg, reply_markup=theme_keyboard)


# Обработка сообщений в режиме модуля
# @bot.message_handler(content_types=["text"])
def mode_answer(m):
    cid = m.chat.id
    # Если включен режим
    if user_mode.get(cid, 0) == MODULE_COMMAND:
        if m.text in dialogs.keys():
            user_theme[cid] = m.text
            talk(m)
        else:
            bot.send_message(cid, 'Такого мы ещё не проходили. Если хочешь выйти из режима, набери /start')


def talk(m):
    cid = m.chat.id
    msgs = dialogs[user_theme[cid]] # список сообщений на тему
    user_answer = m.text if not (m.text.startswith('/') or m.text in dialogs.keys()) else ''
    if user_step[cid] != len(msgs):
        reply = msgs[user_step[cid]].replace('%answer', user_answer)
        bot.send_message(cid, reply, reply_markup=hide_keyoard)
        user_step[cid] += 1
    if user_step[cid] == len(msgs):
        bot.send_message(cid, 'На этом я исчерпан. Если хочешь, давай продолжим в другом режиме (/help)')
        reset_mode(cid)
    else:
        bot.register_next_step_handler_by_chat_id(cid, talk)