import turtle as t
from random import randint

class Border(t.Turtle):
    'Класс границы игрового поля'
    def __init__(self, x1, x2, y1, y2, *, dx=5, dy=5, col='steel blue', ps=5):
        'Здесь происходит создание нового объекта. Назначение атрибутов.'
        super().__init__() # Здесь инициируем всё от класса Turtle
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.color(col)
        self.pensize(ps)
        self.dx = dx # Шаг изменения размера границ
        self.dy = dy
        self.draw()
    
    def draw(self):
        'Метод рисует границы'
        t.tracer(0) # отключить анимацию
        self.penup()
        self.hideturtle()
        self.clear()
        self.goto(self.x1, self.y1)
        self.pendown()
        self.goto(self.x1, self.y2)
        self.goto(self.x2, self.y2)
        self.goto(self.x2, self.y1)
        self.goto(self.x1, self.y1)
        t.update() # и показать сразу отрисованные границы
        t.tracer(1) # Вернуть трассировку
    
    def change_range(self, x1, x2, y1, y2):
        'Метод изменяет размеры границ'
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.draw()

    # Другой способ изменения границ (супер короткая запись. Так обычно не приветсвуется)
    def dec_width(self): self.x1 += self.dx; self.x2 -= self.dx; self.draw()
    def inc_width(self): self.x1 -= self.dx; self.x2 += self.dx; self.draw()
    def dec_heigh(self): self.y1 += self.dy; self.y2 -= self.dy; self.draw()
    def inc_heigh(self): self.y1 -= self.dy; self.y2 += self.dy; self.draw()


class Ball(t.Turtle):
    'Класс шар'
    def __init__(self, border: Border, *, x=0, y=0, dx=0, dy=0, gravity=0.25, shape='circle', col='red', ps=1):
        super().__init__()
        self.penup()
        if x or y:
            self.hideturtle()
            self.goto(x,y)
            self.showturtle()
        self.border = border
        self.shape(shape)
        self.color(col)
        self.pensize(ps)
        self.dx = dx
        self.dy = dy
        self.speed(0)
        self.gravity = gravity

    def next_step(self):
        'Двигает шар на следующий шаг по dx, dy'
        x, y = self.position()
        # Применим гравитацию
        if self.gravity:
            self.dy -= self.gravity
        # Проверим границы
        if x + self.dx <= self.border.x1 or x + self.dx >= self.border.x2:
            self.dx = -self.dx
        if y + self.dy <= self.border.y1 or y + self.dy >= self.border.y2:
            self.dy = -self.dy
        x += self.dx
        y += self.dy
        # Если всё равно наш остался за пределами границы,
        # то придать ему бОльшее ускорение в сторону от стены, чтобы он выскочил
        if (out_dist := x - self.border.x1) < 0 or (out_dist := x - self.border.x2) > 0: 
            self.dx -= out_dist
            x       -= out_dist
        if (out_dist := y - self.border.y1) < 0 or (out_dist := y - self.border.y2) > 0:
            self.dy -= out_dist
            y       -= out_dist
        self.goto(x, y)
        # Если шары слишком быстро летают, то будем их притормаживать
        if not (-10 < self.dx < 10): self.dx -= 0.25 * (-1 if self.dx < 0 else 1)
        if self.dy > 10: self.dy -= 0.25 * (-1 if self.dy < 0 else 1)


    def switch_penup(self):
        'Переключает режим рисования'
        if self.isdown():
            self.penup()
        else:
            self.pendown()

    # Изменяет приращение
    def inc_dx(self): self.dx += 1
    def dec_dx(self): self.dx -= 1
    def inc_dy(self): self.dy += 1
    def dec_dy(self): self.dy -= 1

    # Изменение гравитации
    def more_gravity(self): self.gravity += 0.25
    def less_gravity(self): self.gravity -= 0.25


class Balls():
    'Класс коллекция шаров'
    def __init__(self, border: Border, n: int = 1, *, rand_x_range=0, rand_y_range=0):
        '''В инииализации сразу создаётся нудное количество шаров,
        которые хранятся в списке self.list
        self.selected - Текущий, выделенный шар'''
        n = int(n)
        colors = ('red', 'blue', 'green', 'pink', 'purple', 'yellow', 'brown', 'orange')
        self.list = []
        for i in range(int(n)):
            self.list.append(
                Ball(border,
                    x=randint(-rand_x_range, rand_x_range),
                    y=randint(-rand_y_range, rand_y_range),
                    dx=randint(-5,5), dy=randint(-5,5),
                    shape='circle', 
                    col=colors[randint(0,len(colors)-1)]
                )
            )
        self.selected = self.list[0]
        self.set_play(True)


    def set_play(self, b = True):
        '''Устанавливает артибут продолжения игры
        self.play используется в игровом(основном цикле)'''
        self.play = b


    def select(self, ball: Ball):
        'Выделение шара и снятие выделения с других шаров'
        self.selected = ball
        index_sel = self.list.index(ball)
        for i, ball in enumerate(self.list):
            if i == index_sel:
                ball.shape('square')
            else:
                ball.shape('circle')

    def find_collision(self):
        '''Метод проверяет расстояние между всеми шарами.
        Если расстояние меьше диаметра, то считется столкновение.
        В этом случае рассчитывается новое направление движения шаров.
        Алгоритм взят из интернета на основе механики полностью
        упрогого столкновения'''
        diametr = 20
        # В цикле просмотрим все пары
        for i, ball1 in enumerate(self.list[:-1]):
            for ball2 in self.list[i+1:]:
                x1, y1 = ball1.position()
                x2, y2 = ball2.position()
                dist = ((x1-x2)**2 + (y1-y2)**2)**0.5
                if dist and dist < diametr :
                    a = x1 - x2 # вспомогательные переменные типа extended
                    b = y1 - y2
                    p1 = a*b / dist**2
                    p2 = (a/dist)**2
                    p3 = (b/dist)**2
                    d1 = ball1.dy * p1 + ball1.dx * p2 - ball2.dy * p1 - ball2.dx * p2
                    d2 = ball1.dx * p1 + ball1.dy * p3 - ball2.dx * p1 - ball2.dy * p3
                    ball1.dx -= d1 # меняем значение приращения координаты шаров при движении
                    ball1.dy -= d2
                    ball2.dx += d1
                    ball2.dy += d2
                    #при соударении шары всегда "проникают" друг в друга, поэтому раздвигаем их
                    p3 = (diametr-dist)/2
                    p1 = p3 * (a/dist)
                    p2 = p3 * (b/dist)
                    ball1.goto(x1 + p1, y1 + p1)
                    ball2.goto(x2 - p1, y2 - p1)



##################################
# 
# Основная программа
# 
##################################


border = Border(-150, 150, -150, 150)
n = t.numinput('Запрос', 'Введите количество шаров:')
balls = Balls(border, n, rand_x_range=100, rand_y_range=100) # Список шаров
# Определяем все события взаимодействия с игроком
t.listen() # Нужно для отлавливания нажатия клавиш


def register_caps(func, key):
    'Функция регистрируе события для режима CapsLock'
    # Можно было бы ещё добавить и русскую раскладку, если бы она поддерживалась
    t.onkeypress(func, key.lower())
    t.onkeypress(func, key.upper())

# Управление бордюром
register_caps(lambda: border.inc_heigh(), 'w')
register_caps(lambda: border.dec_heigh(), 's')
register_caps(lambda: border.inc_width(), 'd')
register_caps(lambda: border.dec_width(), 'a')

# Управление направлением мяча
t.onkeypress(lambda: balls.selected.inc_dy(), 'Up')
t.onkeypress(lambda: balls.selected.dec_dy(), 'Down')
t.onkeypress(lambda: balls.selected.inc_dx(), 'Right')
t.onkeypress(lambda: balls.selected.dec_dx(), 'Left')

# Управление скоростью шаров
'''
Здесь хитрым образом задаём два параметра в безымянной функции,
несмотря на то, что она поддерживает только одно выражение.
t.delay(задержка медлу отрисовками в мс) or t.tracer(отрисовывать каждый n-ый шаг)
Используем or или and в зависимости от того что возвращает функция.
В нашем случае t.delay возвращает None, значит, чтобы вычислялость второе выражение,
Нужно использовать or, т.к. для определения результата интерпретатору нужно дойти до первого
не ложного значения или проити до конца и убедиться, что все выражения ложные.
Если бы наша функция возвращала что-то не нулевое, то нужно было бы использовать and,
т.к. для определения результата интерпретатору придётся искать первое ложное высказываение
или перебирать до конца.
'''
t.onkeypress(lambda: t.delay(50) or t.tracer(1), '1') 
t.onkeypress(lambda: t.delay(15) or t.tracer(1), '2')
t.onkeypress(lambda: t.delay(5) or t.tracer(1), '3')
t.onkeypress(lambda: t.delay(1) or t.tracer(1), '4')
t.onkeypress(lambda: t.delay(0) or t.tracer(1), '5')
t.onkeypress(lambda: t.delay(0) or t.tracer(4), '6')
t.onkeypress(lambda: t.delay(0) or t.tracer(16), '7')
t.onkeypress(lambda: t.delay(0) or t.tracer(64), '8')
t.onkeypress(lambda: t.delay(0) or t.tracer(256), '9')
t.onkeypress(lambda: t.delay(0) or t.tracer(1024), '0')

# Рисование
# Для выделенного шара
register_caps(lambda: balls.selected.switch_penup(), 'z')
register_caps(lambda: balls.selected.clear(), 'c')
# Для всех шаров
t.onkeypress(lambda: [ball.switch_penup() for ball in balls.list], 'space')
t.onkeypress(lambda: [ball.clear() for ball in balls.list], 'BackSpace')

# Гравитация
t.onkeypress(lambda: [ball.less_gravity() for ball in balls.list], '-')
t.onkeypress(lambda: [ball.more_gravity() for ball in balls.list], '+')

# Выделение мяча
for ball in balls.list:
    ball.onclick(lambda x,y: balls.select(ball))

# Выход
t.onkeypress(lambda: balls.set_play(False), 'Escape')

# Основной игровой цикл
while balls.play:
    for ball in balls.list:
        ball.next_step()
    balls.find_collision()