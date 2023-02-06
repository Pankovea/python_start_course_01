# Функция добавления режима
MODULE_COMMAND = 'team_register'
MODULE_DESC = 'Регистрация команды студентов'
MODULE_HI = 'Вы вошли в режим: регистрация команды студентов'


def initialize(outer_bot, commands, outer_user_mode):
    global user_mode
    global bot
    global steps
    global user_step
    global user_answers
    user_mode = outer_user_mode
    bot = outer_bot
    commands[MODULE_COMMAND] = MODULE_DESC
    bot.register_message_handler(callback=module_start_command, commands=[MODULE_COMMAND])
    steps = {
        'Введите название команды:': get_teem_name,
        'Введите количество участников:': get_count_students,
        'Введите имя участника:': get_names,
        'Введите пароль:': get_pass_teem,
        }
    user_step = {}
    user_answers = {}

    # Зарегистрировать функции для всех шагов
    for i, _ in enumerate(steps):
        eval('bot.register_message_handler(callback=get_user_step_func('+str(i)+'), content_types=["text"],' + 
            'func=lambda m: user_mode.get(m.chat.id, None) == MODULE_COMMAND and user_step[m.chat.id] == '+str(i)+')')


def get_user_step_text(cid): 
    key = list(steps.keys())[user_step[cid]]
    return key

def get_user_step_func(step): 
    key = list(steps.keys())[step]
    return steps[key]

def next_step_question(cid):
    user_step[cid] += 1
    bot.send_message(cid, get_user_step_text(cid))


# Функция, обрабатывающая команду /MODULE_COMMAND
def module_start_command(m):
    cid = m.chat.id
    user_mode[cid] = MODULE_COMMAND
    user_step[cid] = 0
    bot.send_message(cid, MODULE_HI + '\n\n' + get_user_step_text(cid))


def reset_steps(cid):
    user_step.pop(cid, None)
    user_answers.pop(cid, None)


#### Рабочие функции модуля

def get_teem_name(message):
    '''1. Ввести название команды.
    Запрашивает название команды и возвращает строку'''
    user_answers[message.chat.id] = {'name': message.text}
    next_step_question(message.chat.id)

def get_count_students(message):
    '''Запрашивает количество участников
    Проверяет на соответсвие требованиям  < 2 or > 8
    возврачает целое число
    '''
    teem_count = message.text
    teem_count = int(teem_count) if teem_count.isdecimal() else 0
    if teem_count < 2 or teem_count > 8:
        bot.send_message(message.chat.id ,'Недопустимое количество участников')
        user_step[message.chat.id] -= 1
        next_step_question(message.chat.id)
    else:
        user_answers[message.chat.id]['teem_count'] = teem_count


def get_names(n: int) -> str:
    '''Запрашивает имена участников
    Формирует из первых букв логин и возвращает
    логин -> строка
    '''
    login = ''
    for i in range(n):
        name = input('Введите название участника: ')
        login += name.lower()[0]
    print('Ваш логин:', login)
    return login


def get_pass_teem():
    '''Запрашивает пароль
    Проверяет на соответствие требованиям
    1. отсутсвие символов #%&@/
    2. Длина пароля >= 8
    возвращает пароль -> строка
    '''
    pw = input('Введите пароль: ')
    wrong = '#%&@/'
    if len(pw)<8:
        print('Слишком короткий пароль')
        pw = get_pass_teem()
    for s in pw:
        if s in wrong:
            print('Найден запрещённый символ', s)
            pw = get_pass_teem()
            break
    return pw


def set_points(n: int) -> int:
    '''Производит начисление бонусных баллов команде
    по 200 за каждого члена.
    возвращает число баллов -> int
    '''
    count = n * 200
    print('Вам начислено',count,'баллов')
    return count
