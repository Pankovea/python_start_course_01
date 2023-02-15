# Переменные для пользователей
 # Здесь будем ранить объекты класса Botuser

# Создадим класс для пользователей, где будем хранить всё необходимое
class Botuser:  # Название класса пишем с большой буквы

    all_users = [] # Эта переменная принадлежит всему классу объектов.
                # к ней будем обращаться не через объект, а через класс: Botuser.get_all_id()

    def __init__(self, chat_id: int, user_mode: str = ''): # функция запускается при создании экзепляра класса
        self.id = chat_id            # назначаем переменные создаваемого объекта
        self.mode = user_mode
        self.__step = 0         # Просто инициируем, назначаем начальное значение переменным
        self.__answers = []     # __ перед переменной охначет, что переменную нельзя изменить напрямую 
                                # только через функции 
        Botuser.all_users.append(self) # Записываем нашего пользователя в общий список
    
    def next_step(self) -> None:
        'Следующий шаг'
        self.step += 1

    def prev_step(self) -> None:
        'Предыдущий шаг'
        self.step -= 1

    def reset_step(self) -> None:
        'Начать сначала'
        self.step = 0

    def set_answer(self, answer: str) -> None:
        'Записать ответ на текущий шаг'
        self.answers[self.step] = answer

    def get_answer(self, step: int) -> None:
        'Получить ответ на шаг номер step'
        return self.answers[step]
    
    def reset_mode(self) -> None:
        'Сбросить режим'
        self.mode = ''
        self.step = 0
        self.answers = []

    # следующие функции предназначены для вызова через класс
    def get_all_id(self = None):
        'Возвращает список всех id пользователей'
        return [user.id for user in Botuser.all_users]
    
    def get_user(cid: int):
        'Возвращает объект Botuser'
        i = Botuser.get_all_id().index(cid)
        return Botuser.all_users[i]
