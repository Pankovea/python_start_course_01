from users import botuser
from modules.handlers import BotHandlers

# Функция добавления режима
MODULE_COMMAND = 'team_register'
MODULE_DESC = 'Регистрация команды студентов'
MODULE_HI = 'Вы вошли в режим: регистрация команды студентов'


bh = BotHandlers()
def initialize(outer_bot):
    global bh
    global bot
    bot = outer_bot
    bot.commands[MODULE_COMMAND] = MODULE_DESC
    bh.add_handlers(bot)
    del bh

def next_step_question(user):
    bot.send_message(user.id, user.next_step().get_step_text())

# Функция, обрабатывающая команду /MODULE_COMMAND
@bh.message_handler(commands=[MODULE_COMMAND],
                    func= lambda m: botuser(m.chat.id))
def module_start_command(m):
    cid = m.chat.id
    user = botuser(cid).set_mode(MODULE_COMMAND).set_steps([
        'Введите название команды:',
        'Введите количество участников:',
        'Введите имя участника:',
        'Введите пароль:',
    ])
    bot.send_message(cid, MODULE_HI + '\n\n' + user.get_step_text())


#### Рабочие функции модуля
@bh.message_handler(content_types=["text"],
                    func=lambda m: (user:=botuser(m.chat.id))
                        and user.get_mode() == MODULE_COMMAND
                        and user.get_step() == 0)
def get_teem_name(message):
    '''1. Ввести название команды.
    Запрашивает название команды и возвращает строку'''
    cid = message.chat.id
    user = botuser(cid).set_answer('team_name', message.text)
    next_step_question(user)


@bh.message_handler(content_types=["text"],
                    func=lambda m: (user:=botuser(m.chat.id))
                        and user.get_mode() == MODULE_COMMAND
                        and user.get_step() == 1)
def get_count_students(message):
    '''Запрашивает количество участников
    Проверяет на соответсвие требованиям  < 2 or > 8
    возврачает целое число
    '''
    cid = message.chat.id
    teem_count = message.text
    teem_count = int(teem_count) if teem_count.isdecimal() else 0
    if teem_count < 2 or teem_count > 8:
        bot.send_message(cid,'Недопустимое количество участников')
        user.prev_step()
        next_step_question(user)
    else:
        user = botuser(cid).set_answer('teem_count', teem_count)
        next_step_question(user)


@bh.message_handler(content_types=["text"],
                    func=lambda m: (user:=botuser(m.chat.id))
                        and user.get_mode() == MODULE_COMMAND
                        and user.get_step() == 2)
def get_names(message) -> str:
    '''Запрашивает имена участников
    Формирует из первых букв логин и возвращает
    логин -> строка
    '''
    cid = message.chat.id
    user = botuser(cid)
    n = user.get_answer('teem_count') # количество участников
    if not user.get_answer('name_student'):
        user.set_answer('name_student', [])
    user.get_answer('name_student').append(message.text)
    if len(user.get_answer('name_student')) < n:
        user.prev_step()
        next_step_question(user)
    else:
        login = ''
        for name in user.get_answer('name_student'):
            login += name.lower()[0]
        bot.send_message(cid, 'Ваш логин: ' + login)
        user.set_answer('login', login)
        next_step_question(user)


@bh.message_handler(content_types=["text"],
                    func=lambda m: (user:=botuser(m.chat.id))
                        and user.get_mode() == MODULE_COMMAND
                        and user.get_step() == 3)
def get_pass_teem(message):
    '''Запрашивает пароль
    Проверяет на соответствие требованиям
    1. отсутсвие символов #%&@/
    2. Длина пароля >= 8
    '''
    cid = message.chat.id
    user = botuser(cid)
    pw = message.text
    wrong = '#%&@/'
    pw_is_ok = True
    if len(pw)<8:
        pw_is_ok = False
        bot.send_message(cid, 'Слишком короткий пароль')
    for s in pw:
        if s in wrong:
            pw_is_ok = False
            bot.send_message(cid, 'Найден запрещённый символ ' + s)
            break
    if pw_is_ok:
        user.set_answer('password', pw)
        set_points(user)
    else:
        user.prev_step()
        next_step_question(user)


def set_points(user):
    '''Производит начисление бонусных баллов команде
    по 200 за каждого члена.
    '''
    n = user.get_answer('teem_count')
    points_count = n * 200
    user.set_answer('points_count', points_count)
    bot.send_message(user.id, f'Вам начислено {points_count} баллов')
    bot.send_message(user.id, 'Программа завершена. /help\nВаши ответы:\n' + user.get_answers_str())
    user.reset_mode()