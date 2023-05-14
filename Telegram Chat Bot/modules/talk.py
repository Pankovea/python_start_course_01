# import telebot
from telebot import types
from modules.handlers import BotHandlers
from users import botuser


# Функция добавления режима
MODULE_COMMAND = 'talk'
MODULE_HI = 'Вы вошли в режим: Общение'

bh = BotHandlers()
def initialize(outer_bot):
    global bh
    global bot
    bot = outer_bot
    bot.commands[MODULE_COMMAND] = 'Начать общаться'
    bh.add_handlers(bot)
    del bh


# Объявляем переменные модуля
user_theme = {}

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
@bh.message_handler(commands=[MODULE_COMMAND],
                    func= lambda m: botuser(m.chat.id))
def module_start_command(m):
    cid = m.chat.id
    # т.к. методы класса воздвращают объект класса, то можем объединять методы в цепочку
    user = botuser(cid).set_mode(MODULE_COMMAND)
    msg = 'Хорошо, давай пообщаемся. Что тебя интересует:\n'
    for theme in dialogs.keys():
        msg += theme + '\n'
    bot.send_message(cid, msg, reply_markup=theme_keyboard)


# Обработка сообщений в режиме модуля
@bh.message_handler(content_types=["text"],
                    func=lambda m: (user:=botuser(m.chat.id))
                    and user.get_mode() == MODULE_COMMAND)
def mode_answer(m):
    cid = m.chat.id
    if m.text in dialogs.keys():
        user_theme[cid] = m.text
        talk(m)
    else:
        bot.send_message(cid, 'Такого мы ещё не проходили. Если хочешь выйти из режима, набери /start')


def talk(m):
    cid = m.chat.id
    user = botuser(cid)
    msgs = dialogs[user_theme[cid]] # список сообщений на тему
    user_answer = m.text if not (m.text.startswith('/') or m.text in dialogs.keys()) else ''
    if user.get_step() != len(msgs):
        reply = msgs[user.get_step()].replace('%answer', user_answer)
        bot.send_message(cid, reply, reply_markup=hide_keyoard)
        user.next_step()
        
    if user.get_step() == len(msgs):
        bot.send_message(cid, 'На этом я исчерпан. Давай продолжим в другом режиме (/help)')
        user.reset_mode()
    else:
        bot.register_next_step_handler_by_chat_id(cid, talk)