# Функция добавления режима
MODULE_COMMAND = 'online_trener'
MODULE_HI = 'Вы вошли в режим: Онлайн тренер'


def initialize(outer_bot, commands, outer_user_mode):
    global user_mode
    global bot
    global steps
    global user_step
    global user_answers
    user_mode = outer_user_mode
    bot = outer_bot
    commands[MODULE_COMMAND] = 'Онлайн тренер'
    bot.register_message_handler(callback=module_start_command, commands=[MODULE_COMMAND])
    steps = {
        'Введите ваше имя:': input_name,
        'Ваш возраст:': input_age,
        'Вес (кг):': input_weight,
        'Рост (см):': input_height,
        'Ваш желаемый вес': input_new_weight,
        # 'Ответ': desired_result,
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


def input_name(m):
    global name
    name = m.text
    next_step_question(m.chat.id)
    
def input_age(m):
    global age
    age = int2(m.text)
    reg(m.chat.id, name, age)
    next_step_question(m.chat.id)

def reg(cid, name, age):
    msg="Пользователь " + name + " c возрастом " + str(age) + " зарегистрирован!"
    bot.send_message(cid, msg)

def int2(s):
    return int(s) if s.isnumeric() else 0

def input_weight(m):
    global weight
    weight = int2(m.text)
    next_step_question(m.chat.id)

def input_height(m):
    global height
    height = int2(m.text) / 100
    if age < 18:
        imt_child(m.chat.id)
    else:
        imt_v(m.chat.id)


def imt_child(cid):
    global IMT
    bot.send_message(cid, "Запущена детская программа")
    IMT = weight/(height**2)
    if IMT <= 15.1:
        bot.send_message(cid, "Дефицит массы")
        IMT = -1
    elif 15.2 < IMT < 22:
        bot.send_message(cid, "Нормальный вес")
        IMT = 0
    elif IMT > 22:
        bot.send_message(cid, "Лишний вес")
        IMT = 1
    next_step_question(cid) # Ваш желаемый вес:


def imt_v(cid):
    global IMT
    bot.send_message(cid, "Запущена взрослая программа")
    IMT = weight / (height ** 2)
    if IMT <= 18.4:
        bot.send_message(cid, "Дефицит массы")
        IMT = -1
    elif 18.5 < IMT < 25:
        bot.send_message(cid, "Нормальный вес")
        IMT = 0
    elif IMT > 25:
        bot.send_message(cid, "Лишний вес")
        IMT = 1
    next_step_question(cid) # Ваш желаемый вес:


def input_new_weight(m):
    global new_weight
    new_weight = int2(m.text)
    desired_result(m.chat.id, IMT, new_weight, weight)


def desired_result(cid, IMT, result, weight):
    if result > weight and IMT == -1:
        bot.send_message(cid, "Наберём " + str(result - weight) + " кг")
    elif result < weight and IMT == 1:
        bot.send_message(cid, "Похудеем на " + str(weight - result) + " кг")
    else:
        bot.send_message(cid, "Рекомендую программу для улучшения тела с небольшим изменением веса\nПрограмма завершена")
    reset_steps(cid)

def reset_steps(cid):
    user_step.pop(cid, None)
    user_answers.pop(cid, None)



                        
