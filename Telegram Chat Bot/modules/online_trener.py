from users import *

# Функция добавления режима
MODULE_COMMAND = 'online_trener'
MODULE_HI = 'Вы вошли в режим: Онлайн тренер'


def initialize(outer_bot):
    global bot
    global steps
    bot = outer_bot
    bot.commands[MODULE_COMMAND] = 'Онлайн тренер'
    bot.register_message_handler(callback=module_start_command, commands=[MODULE_COMMAND])
    steps = {
        'Введите ваше имя:': input_name,
        'Ваш возраст:': input_age,
        'Вес (кг):': input_weight,
        'Рост (см):': input_height,
        'Ваш желаемый вес': input_new_weight,
        # 'Ответ': desired_result,
        }
    # Зарегистрировать функции-обработчики для всех шагов
    for i, _ in enumerate(steps):
        eval(f'''bot.register_message_handler(callback=get_user_step_func({i}), content_types=["text"],
                    func=lambda m: botuser(m.chat.id).get_mode() == MODULE_COMMAND
                               and botuser(m.chat.id).get_step() == {i})''')


def get_user_step_text(cid): 
    step = botuser(cid).get_step()
    text = list(steps.keys())[step]
    return text

def get_user_step_func(step): 
    key = list(steps.keys())[step]
    return steps[key]

def next_step_question(cid):
    botuser(cid).next_step()
    bot.send_message(cid, get_user_step_text(cid))


# Функция, обрабатывающая команду /MODULE_COMMAND
def module_start_command(m):
    cid = m.chat.id
    botuser(cid).set_mode(MODULE_COMMAND)
    bot.send_message(cid, MODULE_HI + '\n\n' + get_user_step_text(cid))


def input_name(m):
    cid = m.chat.id
    # т.к. методы класса воздвращают объект класса, то можем объединять методы в цепочку
    botuser(cid).set_answer('name', m.text).next_step()
    bot.send_message(cid, get_user_step_text(cid))
    
def input_age(m):
    cid = m.chat.id
    user = botuser(cid)
    age = int2(m.text)
    user.set_answer('age', age)
    reg(cid, user.get_answer('name'), age)
    next_step_question(cid)

def reg(cid, name, age):
    msg = f"Пользователь {name} c возрастом {age} зарегистрирован!"
    bot.send_message(cid, msg)

def int2(s):
    return int(s) if s.isnumeric() else 0

def input_weight(m):
    cid = m.chat.id
    botuser(cid).set_answer('weight', int2(m.text))
    next_step_question(cid)

def input_height(m):
    cid = m.chat.id
    height = int2(m.text) / 100
    user = botuser(cid)
    user.set_answer('height', height)
    if user.get_answer('age') < 18:
        imt_child(cid, user.get_answer('weight'), height)
    else:
        imt_v(cid, user.get_answer('weight'), height)


def imt_child(cid, weight, height):
    user = botuser(cid)
    # переменную можно записать прямо в объект класса
    user.imt = weight/(height**2)
    bot.send_message(cid, "Запущена детская программа")
    if imt <= 15.1:
        bot.send_message(cid, "Дефицит массы")
        imt = -1
    elif 15.2 < imt < 22:
        bot.send_message(cid, "Нормальный вес")
        imt = 0
    elif user.imt > 22:
        bot.send_message(cid, "Лишний вес")
        imt = 1
    bot.send_message(cid, get_user_step_text(cid))
    next_step_question(cid) # Ваш желаемый вес:


def imt_v(cid, weight, height):
    user = botuser(cid)
    user.imt = weight / (height ** 2)
    bot.send_message(cid, "Запущена взрослая программа")
    if user.imt <= 18.4:
        bot.send_message(cid, "У Вас дефицит массы")
        user.imt = -1
    elif 18.5 < user.imt < 25:
        bot.send_message(cid, "У Вас нормальный вес")
        user.imt = 0
    elif user.imt > 25:
        bot.send_message(cid, "У Вас лишний вес")
        user.imt = 1
    next_step_question(cid) # Ваш желаемый вес:


def input_new_weight(m):
    cid = m.chat.id
    user = botuser(cid)
    new_weight = int2(m.text)
    botuser(cid).set_answer('new_weight', int2(m.text))
    desired_result(cid, user.imt, new_weight, user.get_answer('weight'))


def desired_result(cid, imt, result, weight):
    if result > weight and imt == -1:
        bot.send_message(cid, "Наберём " + str(result - weight) + " кг")
    elif result < weight and imt == 1:
        bot.send_message(cid, "Похудеем на " + str(weight - result) + " кг")
    else:
        bot.send_message(cid, "Рекомендую программу для улучшения тела с небольшим изменением веса")
    msg = 'Программа завершена.\nВаши ответы:\n' + botuser(cid).get_answers_str()
    bot.send_message(cid, msg)
    botuser(cid).reset_mode()

