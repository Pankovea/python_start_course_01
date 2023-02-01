import datetime

# Функция для вывода диалога в консоль
def listener(messages):
    """
    Когда приходят новые сообщения, они будут выводиться в консоль
    """
    for m in messages:
        if m.content_type == 'text':
            # вывести присланноое сообщение в консоль
            print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"), str(m.chat.first_name), "[" + str(m.chat.id) + "]: " + m.text)


def register_listener(bot):
    bot.set_update_listener(listener)  # зарегистрировать вывод сообщений