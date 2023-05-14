# Функция для быстрого доступа к объекту класса по его chat_id
# функции пишем с маленькой буквы
def botuser(cid: int) -> 'Botuser':
    'Возвращает объект Botuser по его chat_id'
    return Botuser.getme(cid)


# Создадим класс для пользователей, где будем хранить всё необходимое
class Botuser:  # Название класса пишем с большой буквы

    __all_users = set() # Эта переменная принадлежит всему классу объектов.
                # к ней будем обращаться не через объект, а через класс: Botuser.get_all_id()

    def __init__(self, chat_id: int, user_mode: str = ''): # функция запускается при создании экзепляра класса
        self.__id = chat_id            # назначаем переменные создаваемого объекта
        self.__mode = user_mode
        self.__step = 0         # Просто инициируем, назначаем начальное значение переменным
        self.__steps = []       # Здесь храним текст шагов
        self.__answers = {}     # __ перед переменной охначет, что переменную нельзя изменить напрямую 
                                # только через функции 
        Botuser.__all_users.add(self)   # Если пользователь новый, то добавим в множество

    @property
    def id(self):
        return self.__id

    def get_step(self):
        'Возвращает текущий шаг пользователя'
        return self.__step

    def set_steps(self, steps):
        'Сохраняет шаги'
        self.__steps = steps
        return self

    def get_step_text(self):
        'Возвращает текст текущего шага пользователя'
        if len(self.__steps) > self.__step:
            return self.__steps[self.__step]

    def next_step(self):
        'Переходит на следующий шаг'
        self.__step += 1
        return self

    def prev_step(self):
        'Переходит на предыдущий шаг'
        self.__answers.pop(self.__step, None) # Удаляет ответ, если он записан
        self.__step -= 1
        return self

    def reset_step(self):
        'Начать сначала'
        self.__step = 0
        self.__answers = {}
        return self

    # Сеттеры и геттеры нужны для того,
    # чтобы избежать нарушения внутренней логики прямым назначением из вне.
    def set_answer(self, variable: str = None, answer: str | int = ''):
        'Записать ответ на текущий шаг'
        if not variable:
            variable = self.__step
        self.__answers[variable] = answer
        return self

    def get_answer(self, step_variable: int | str):
        '''Получить ответ на шаг номер step или переменную variable
        В случае если нет индекса, возвращает None'''
        return self.__answers.get(step_variable)

    def get_answers_list(self):
        'Получить список всех ответов'
        return list(self.__answers.values())

    def get_answers_dict(self):
        'Получить словарь ответов'
        return self.__answers.copy()

    def get_answers_str(self):
        'Возвращает строку с шагами и ответами'
        s = ''
        for step, ans in self.__answers.items():
            s += f'{step}: {ans}\n'
        return s

    def get_mode(self):
        return self.__mode

    def set_mode(self, mode: str):
        'Установить режим'
        self.__mode = mode
        self.__step = 0
        self.__steps = []
        self.__answers = {}
        return self

    def reset_mode(self):
        'Сбросить режим'
        self.reset_step()
        self.steps = []
        self.set_mode('')
        return self

    # следующие функции предназначены для вызова через класс Botuser
    @classmethod
    def get_all_id(cls):
        'Возвращает список всех id пользователей'
        return [user.__id for user in cls.__all_users]

    @classmethod
    def getme(cls, cid: int):
        'Возвращает объект Botuser по его chat_id'
        for user in cls.__all_users:
            if user.__id == cid:
                return user
