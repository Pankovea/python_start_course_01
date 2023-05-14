from users import botuser
from modules.handlers import BotHandlers

# Функция добавления режима
MODULE_COMMAND = 'online_trener'
MODULE_HI = 'Вы вошли в режим: Онлайн тренер'


bh = BotHandlers()
def initialize(outer_bot):
    global bh
    global bot
    bot = outer_bot
    bot.commands[MODULE_COMMAND] = 'Онлайн тренер'
    bh.add_handlers(bot)
    del bh
    


# Функция, обрабатывающая команду /MODULE_COMMAND
@bh.message_handler(commands=[MODULE_COMMAND],
                    func= lambda m: botuser(m.chat.id))
def module_start_command(m):
    cid = m.chat.id
    # т.к. методы класса воздвращают объект класса, то можем объединять методы в цепочку
    user = botuser(cid).set_mode(MODULE_COMMAND).set_steps([
        'Введите ваше имя:',
        'Ваш возраст:',
        'Вес (кг):',
        'Рост (см):',
        'Ваш желаемый вес',
    ])
    bot.send_message(cid, MODULE_HI + '\n\n' + user.get_step_text()) # Введите ваше имя:



@bh.message_handler(content_types=["text"],
                    func=lambda m: (user:=botuser(m.chat.id))
                        and user.get_mode() == MODULE_COMMAND
                        and user.get_step() == 0)
def input_name(m):
    cid = m.chat.id
    # т.к. методы класса воздвращают объект класса, то можем объединять методы в цепочку
    user = botuser(cid).set_answer('name', m.text)
    bot.send_message(cid, user.next_step().get_step_text()) # Ваш возраст:



def int_(s):
    return int(s) if s.isnumeric() else 0


@bh.message_handler(content_types=["text"],
                    func=lambda m: (user:=botuser(m.chat.id))
                        and user.get_mode() == MODULE_COMMAND
                        and user.get_step() == 1)
def input_age(m):
    cid = m.chat.id
    age = int_(m.text)
    user = botuser(cid).set_answer('age', age)
    reg(cid, user.get_answer('name'), age)
    bot.send_message(cid, botuser(cid).next_step().get_step_text()) # Вес (кг):


def reg(cid, name, age):
    msg = f"Пользователь {name} c возрастом {age} зарегистрирован!"
    bot.send_message(cid, msg)



@bh.message_handler(content_types=["text"],
                    func=lambda m: (user:=botuser(m.chat.id))
                        and user.get_mode() == MODULE_COMMAND
                        and user.get_step() == 2)
def input_weight(m):
    cid = m.chat.id
    user = botuser(cid).set_answer('weight', int_(m.text))
    bot.send_message(cid, user.next_step().get_step_text()) # Рост (см):



@bh.message_handler(content_types=["text"],
                    func=lambda m: (user:=botuser(m.chat.id))
                        and user.get_mode() == MODULE_COMMAND
                        and user.get_step() == 3)
def input_height(m):
    cid = m.chat.id
    height = int_(m.text) / 100
    user = botuser(cid).set_answer('height', height)
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
    bot.send_message(cid, user.next_step().get_step_text()) # Ваш желаемый вес:


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
    bot.send_message(cid, user.next_step().get_step_text()) # Ваш желаемый вес:



@bh.message_handler(content_types=["text"],
                    func=lambda m: (user:=botuser(m.chat.id))
                        and user.get_mode() == MODULE_COMMAND
                        and user.get_step() == 4)
def input_new_weight(m):
    cid = m.chat.id
    user = botuser(cid)
    new_weight = int_(m.text)
    botuser(cid).set_answer('new_weight', int_(m.text))
    desired_result(cid, user.imt, new_weight, user.get_answer('weight'))


def desired_result(cid, imt, result, weight):
    if result > weight and imt == -1:
        bot.send_message(cid, "Наберём " + str(result - weight) + " кг")
    elif result < weight and imt == 1:
        bot.send_message(cid, "Похудеем на " + str(weight - result) + " кг")
    else:
        bot.send_message(cid, "Рекомендую программу для улучшения тела с небольшим изменением веса")
    bot.send_message(cid, 'Программа завершена. /help\nВаши ответы:\n' + botuser(cid).get_answers_str())
    botuser(cid).reset_mode()

