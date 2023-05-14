import turtle
from turtle import Turtle, done, bye
from random import randint
import time
from tkinter import Button

# Для моментального обновления экрана
turtle.hideturtle()
turtle.tracer(0)

# Зарегистрировать новую форму черепашки
key_shape = ((-10, -10), (-2, -10), (-2, -8), (0, -8), (0, -5), (3, -5), (3, -2),
             (6, -2), (10, 2), (10, 6), (6, 10), (1, 10), (-2, 7), (-2, 3), (-10, -5), (-10, -10)) 
turtle.register_shape('key', key_shape)

dog_shape = ( (-2.3,9.3),(-2.3,9.3),(-3.4,7.8),(-2.8,5.7),(0,5.7),(2.8,5.7),(3.4,7.8),(2.3,9.3),(2.3,9.3),(3.1,10.4),(4.8,8.1),(3.8,4.7),(5.5,4.7),(
	6.6,3.9),(5.6,0.6),(4.5,0.6),(3.5,-3),(4.6,-4),(3.5,-7.6),(2,-7.6),(0.5,-9.6),(-0.5,-9.6),(-2,-7.6),(-3.5,-7.6),(-4.6,-4),(-3.5,-3),(-4.5,0.6),(-5.6,0.6),(
	-6.6,3.9),(-5.5,4.7),(-3.8,4.7),(-4.8,8.1),(-3.1,10.4) )

turtle.register_shape('dog', dog_shape)
  


class Sprite(Turtle):
  'Общий класс объекта в игре'
  SIZE = 1
  COLLIDE_DIST = 18
  fps = 30
  calc_fps = 30
  SPD = 150 # Скорость перемещения пикс в секунду
  step = SPD / calc_fps
  update_every_n_frame = 1
  
  def __init__(self, x=0, y=0):
    super().__init__()
    self.speed(0)
    self.penup()
    self.goto(round(x), round(y))
    self.can_move = False
    self.turtlesize(Sprite.SIZE)


  def is_collide(self, other):
    'Определяет столкновение и возвращает вектор направления взаимодействия'
    dist = self.distance(other.xcor(), other.ycor())
    if dist < 2 * self.COLLIDE_DIST * Sprite.SIZE: # Грубый отсев
      if 'custom_collide_shape' in dir(other):
          # Если в другом классе переопределена форма определения столкновения, то использовать её 
          return other.custom_collide_shape(self)
      else:
          return dist < self.COLLIDE_DIST * Sprite.SIZE
    else:
      return False


  def interact_list(self, spr_list: list['Sprite']):
    'Определяет взаимодействие со списком объектов'
    for spr in spr_list:
      self.interact(spr)

  def interact(self, other: 'Sprite'):
    'Определяет взаимодействие'
    if self.is_collide(other):
        self.act(other)
        other.act(self)

  def act(self, other):
    'Дествие спрайта на другой спрайт'
    pass  # В базовом классе нет дейтсвия


class Wall(Sprite):
  'Спрайт стена'
  def __init__(self, x=0, y=0):
    super().__init__(x, y)
    self.shape('square')
    self.color('brown')

  def custom_collide_shape(self, other):
    'Определяет столкновение'
    return (self.xcor() + self.COLLIDE_DIST > other.xcor() and
            self.xcor() - self.COLLIDE_DIST < other.xcor() and
            self.ycor() + self.COLLIDE_DIST > other.ycor() and
            self.ycor() - self.COLLIDE_DIST < other.ycor() )
    
  def act(self, other):
    if other.can_move:
      other.goto(other.xcor() - other.dx,
                 other.ycor() - other.dy)
      other.dx = 0
      other.dy = 0


class WallSkew1(Wall):
  'Спрайт наклонная стена'
  def __init__(self, x=0, y=0):
    super().__init__(x, y)
    self.shearfactor(-1)

  def custom_collide_shape(self, other):
    '''Определяет столкновение пересечением областей,
    ограниченных 6 линиями: vert1 and vert2 and diag1 and diag2 and diag3 and diag4
    self = wall x1, y1
    other = player x2, y2
            \  diag1
             \/|vert2
     x1,y1_1 ..|x1_1,y1_1
            /  |
         \ / . |\  <- x1,y1 = self.xcor(), self.ycor()
          \|  /  \diag3
  x1_2,y1_2|.. x1,y1_2
      vert1|/\
       diag2  \diag4
    '''
    x1 = self.xcor()
    x1_1 = self.xcor() + self.COLLIDE_DIST
    x1_2 = self.xcor() - self.COLLIDE_DIST
    y1_1 = self.ycor() + self.COLLIDE_DIST
    y1_2 = self.ycor() - self.COLLIDE_DIST
    x2 = other.xcor()
    y2 = other.ycor()
    vert1 = x1 + self.COLLIDE_DIST - x2 > 0
    vert2 = x1 - self.COLLIDE_DIST - x2 < 0
    diag1 = x2 - y2 + y1_1 - x1 > 0
    diag2 = x2 - y2 + y1_2 - x1 < 0
    diag3 =-x2 - y2 + y1_1 + x1_1 > 0
    diag4 =-x2 - y2 + y1_2 + x1_2 < 0
    return vert1 and vert2 and diag1 and diag2 and diag3 and diag4



class WallSkew2(Wall):
  'Спрайт наклонная стена'
  def __init__(self, x=0, y=0):
    super().__init__(x, y)
    self.shearfactor(1)

  def custom_collide_shape(self, other):
    """Определяет столкновение
    self = wall x1, y1
    other = player x2, y2
        diag1
      vert1|\ /diag3
           | \ 
  x1_1,y1_1|..\ x1,y1_1
           |   \ /
          /| . |/  <- x1,y1 = self.xcor(), self.ycor()
         / |   |  
    x1,y1_2 \..|x1_2,y1_2
             \ |
            / \|vert2
      diag4/   diag2
    """
    x1 = self.xcor()
    x1_1 = self.xcor() - self.COLLIDE_DIST
    x1_2 = self.xcor() + self.COLLIDE_DIST
    y1_1 = self.ycor() + self.COLLIDE_DIST
    y1_2 = self.ycor() - self.COLLIDE_DIST
    x2 = other.xcor()
    y2 = other.ycor()
    vert1 = x1 + self.COLLIDE_DIST - x2 > 0
    vert2 = x1 - self.COLLIDE_DIST - x2 < 0
    diag1 =-x2 - y2 + y1_1 + x1 > 0
    diag2 =-x2 - y2 + y1_2 + x1 < 0
    diag3 = x2 - y2 + y1_1 - x1_1 > 0
    diag4 = x2 - y2 + y1_2 - x1_2 < 0
    return vert1 and vert2 and diag1 and diag2 and diag3 and diag4
  

class Door(Wall):
  is_open = False
  time_open = 15

  'Спрайт дверь'
  def __init__(self, x=0, y=0):
    super().__init__(x, y)
    self.color('darkblue')

  @classmethod
  def time_step(cls):
    'Счётчик времени, нужно запускать после каждого обновления экрана'
    if cls.is_open:
      cls.time_open -= 1 / super().calc_fps
    if cls.time_open < 0:
      cls.is_open = False
      cls.time_open = 15

  def check_opened(self):
    if self.is_open:
      self.hideturtle()
    if not self.is_open:
      self.showturtle()

  def act(self, other):
    # Блокировать есди закрыта
    if not self.is_open:
        super().act(other)


class Key(Sprite):
  def __init__(self, x=0, y=0):
    super().__init__(x, y)
    self.shape('key')

  def act(self, other: any):
    'Действие дри соприкосновении'
    Door.is_open = True


class Coin(Sprite):
  num_coins = 0

  'Спрайт Монета'
  def __init__(self, x=0, y=0):
    super().__init__(x, y)
    self.color('yellow')
    self.shape('circle')
    self.points = randint(1,10)
    Coin.num_coins += 1

  def act(self, other):
    if self.points:
      other.points += self.points
      self.points = 0
      self.hideturtle()
      Coin.num_coins -= 1



class MoveableSprite(Sprite):
  DIAG_MUL = 0.707

  def __init__(self, x=0, y=0):
    super().__init__(x, y)
    self.dx = 0
    self.dy = 0
    self.can_move = True
  

  def make_step(self):
    if self.dx != 0 or self.dy != 0:
      x_new = self.xcor() + self.dx
      y_new = self.ycor() + self.dy
      self.setheading(self.towards(x_new, y_new))
      self.forward(self.distance(x_new, y_new))


class Player(MoveableSprite):
  def __init__(self, x=0, y=0):
    super().__init__(x, y)
    self.shape('turtle')
    self.color('green')
    self.points = 0

  
  def press_right(self):
    if self.dy:
      self.dx = super().step * super().DIAG_MUL
      if self.dy == super().step: self.dy *= super().DIAG_MUL
    else:
      self.dx = super().step

  def press_left(self):
    if self.dy:
      self.dx = -super().step * super().DIAG_MUL
      if self.dy == super().step: self.dy *= super().DIAG_MUL
    else:
      self.dx = -super().step

  def press_up(self):
    if self.dx:
      self.dy = super().step * super().DIAG_MUL
      if self.dx == super().step: self.dx *= super().DIAG_MUL
    else:
      self.dy = super().step
  
  def press_down(self):
    if self.dx:
      self.dy = -super().step * super().DIAG_MUL
      if self.dx == super().step: self.dx *= super().DIAG_MUL
    else:
      self.dy = -super().step

  def release_right(self): self.dx = 0
  def release_left(self):  self.dx = 0
  def release_up(self):    self.dy = 0
  def release_down(self):  self.dy = 0


class Dog(MoveableSprite):
  col = ['blue', 'purple', 'red']
  def __init__(self, x=0, y=0):
    super().__init__(x, y)
    self.shape('dog')
    self.strong = randint(0, 2)
    self.color(Dog.col[self.strong])
    self.strong = (self.strong + 1) * 3
    self.turtlesize(1.5)


  def make_step(self):
    st = super().step
    # Поворачиваться с вероятностью 10 % 
    if randint(0,100) < 10:
      self.dx = randint(-1,1) * st
    if randint(0,100) < 10:
      self.dy = randint(-1,1) * st
    if self.dx and self.dy: 
      self.dx *= super().DIAG_MUL
      self.dy *= super().DIAG_MUL
    super().make_step()


  def act(self, other):
    if isinstance(other, Player):
        other.points -= self.strong
        self.strong = 0
        self.hideturtle()


class Tablo(Turtle):
  def __init__(self, x=0, y=0, font = ('Arial', 14, 'bold')):
    # Табло с информацией о ходе игры
    super().__init__()
    self.font = font
    self.right(90) # смотреть вниз
    self.hideturtle()
    self.penup()
    self.goto(x,y)

  def show_lines(self, text):
    self.clear()
    lines = text.split('\n')
    for line in lines:
      self.write(line, font=self.font)
      self.fd(20)
    self.bk(len(lines)*20)

  def show_win(self):
    x,y = self.pos()
    self.goto(0,0)
    self.write('Победа!', font=self.font)
    self.goto(x,y)

  def show_loose(self):
    x,y = self.pos()
    self.goto(0,0)
    self.write('Проигрыш :(', font=self.font)
    self.goto(x,y)

  def show_end(self):
    x,y = self.pos()
    self.goto(0,0)
    self.write('Конец')
    self.goto(x,y)


class Level():
  frame = 0
  'Класс уровня'
  def __init__(self, level: list[str], sprites: dict) -> None:
    self.all_sprites: list[Sprite] = []
    self.player: Player = None
    self.coins: list[Coin] = []
    self.dogs: list[Dog]  = []
    self.keys: list[Key]  = []
    self.walls: list[Wall]  = []
    self.doors: list[Door]  = []
    'Пробегаем по всему массиву символов и создаём соответсвующие спрайты'
    for y, row in enumerate(level):
      # self.all_sprites.append([])
      for x, char in enumerate(row):
        CurSpriteClass = sprites[char]
        if CurSpriteClass:
          spr = CurSpriteClass((x - len(row)/2)   * 20 * Sprite.SIZE,
                               (-y + len(level)/2) * 20 * Sprite.SIZE)
          self.all_sprites.append(spr)
          if   char == 'p': self.player = spr
          elif char == '@': self.dogs.append(spr)
          elif char == '*': self.coins.append(spr)
          elif char in ['#', '\\', '/']: self.walls.append(spr)
          elif char == '>': self.doors.append(spr)
          elif char == 'K': self.keys.append(spr)

    self.tablo = Tablo(
      round(len(row)/2 * 20 * Sprite.SIZE + 20),
      round(len(level)/2 * 20 * Sprite.SIZE - 40)
    )
    self.game_info = Tablo(     
      round(-len(row)/2 * 20 * Sprite.SIZE - 140),
      round(-len(level)/2 * 20 * Sprite.SIZE + 100),
      font=('Arial', 10, 'bold')
    )

    # Управление
    scr = self.player.getscreen()
    scr.listen()
    scr.onkeypress(self.player.press_up, 'Up')
    scr.onkeypress(self.player.press_left, 'Left')
    scr.onkeypress(self.player.press_right, 'Right')
    scr.onkeypress(self.player.press_down, 'Down')
    scr.onkeyrelease(self.player.release_up, 'Up')
    scr.onkeyrelease(self.player.release_left, 'Left')
    scr.onkeyrelease(self.player.release_right, 'Right')
    scr.onkeyrelease(self.player.release_down, 'Down')

    # Обновить экран, после прорисовки
    turtle.update()
          

  def start(self):
    Level.time = time.time()
    while Coin.num_coins > 0 and self.player and self.player.points >= 0:
      Level.frame += 1
      frame_start_time = time.time()
      self.player.make_step()
      self.player.interact_list(self.all_sprites)

      for dog in self.dogs:
        dog.make_step()
        dog.interact_list(self.walls)
        dog.interact_list(self.doors)

      Door.time_step()
      if self.doors:
        door_visible = self.doors[0].isvisible()
        if Door.is_open and door_visible:
          # Если дверь открывается, то спрятать их
          for door in self.doors:
            door.check_opened()
        elif not Door.is_open and not door_visible:
          # Если дверь закрывается, то проверить нет ли игрока не дверях
          if sum([1 for door in self.doors if self.player.is_collide(door)]):
            # Если есть, то продлить время открытия
            Door.is_open = True
            Door.time_open = .5
          else:
            # Иначе закрыть двери
            for door in self.doors:
              door.check_opened()

      
      info =  f'Время: {round(time.time() - self.time)}'
      info += f'\nОчки: {self.player.points}'
      info += f'\nДвери: {int(round(Door.time_open,0))}' if Door.is_open else ''
      self.tablo.show_lines(info)

      info  = f'update fps: {int(round(Sprite.fps))}'
      info += f'\ncalc fps: {int(round(Sprite.calc_fps))}'
      info += f'\nskip frames: {Sprite.update_every_n_frame - 1}'
      info += f'\ncalc frames: {int(round(Level.frame))}'
      self.game_info.show_lines(info)

      # Просчёт объектов завершён, осталось обновить экран
      # Рассчитаем время на просчёт и обновление экрана
      # Если в сумме FPS получится меньше 30, то рассчитаем сколько
      # кадров надо пропустить на обновление. Но просчёт всё равно производить
      # чтобы не перескакивать через стены.
      frame_calc_time = time.time() - frame_start_time
      if Level.frame % Sprite.update_every_n_frame == 0:
        # Обновлять каждый update_every_n_frame кадр и пересчитывать fps
        turtle.update()
        frame_total_time = time.time() - frame_start_time
        Sprite.fps = 1 / frame_total_time
        if 1 < Sprite.fps < 30 :
          Sprite.update_every_n_frame = int(30 // Sprite.fps)
        Sprite.calc_fps = 1 / (frame_calc_time * Sprite.update_every_n_frame + frame_total_time) * (Sprite.update_every_n_frame + 1)
        Sprite.step = Sprite.SPD / Sprite.calc_fps
    else:
      for spr in self.all_sprites:
        spr.hideturtle()
      if Coin.num_coins == 0:
        self.tablo.show_win()
      elif self.player and self.player.points < 0:
        self.tablo.show_loose()
      else:
        self.tablo.show_end()
      turtle.update()
      self.end()

  def end(self):
    Coin.num_coins = 0
    Door.is_open = False
    Door.time_open = 15
    Level.frame = 0
    Level.update_every_n_frame = 1
    self.player = None
    self.coins.clear()
    self.dogs.clear()
    self.keys.clear()
    self.walls.clear()
    self.doors.clear()
    self.all_sprites.clear()
    self.game_info.clear()



sprites = {
    ' ': None,       # Пустота
    '#': Wall,       # Стена
    '/': WallSkew1 , # Косая стена
   '\\': WallSkew2 , # Косая стена
    '*': Coin,       # Монета
    '@': Dog,        # Cбакачё
    '>': Door,       # Дверь 
    'K': Key,        # Ключ
    'p': Player,     # Игрок
}


# Уровени
levels = []
levels.append(
   [r'##############################',
    r'#  *          K          *   #',
    r'#                            #',
    r'#>>>>>#               #>>>>>>#',
    r'#     #       #       #      #',
    r'#  @  ####    #    ####  @   #',
    r'#     #       #       #      #',
    r'#  K  #       #       #  K   #',
    r'#>>>>>#       #       #>>>>>>#',
    r'#          #######           #',
    r'#           * # *            #',
    r'#   #>>>>>>>>>#>>>>>>>>>#    #',
    r'#   #                   #    #',
    r'#   #   K     p     K   #    #',
    r'#   #   @           @   #    #',
    r'#   #         *         #    #',
    r'#   #>>>>>>>>>#>>>>>>>>>#    #',
    r'#             #              #',
    r'#           K # K            #',
    r'#             #              #',
    r'#   ######################   #',
    r'#   # *       K        * #   #',
    r'#   #                    #   #',
    r'#        ####   ####         #',
    r'#    @    * #   # *    @     #',
    r'#           #   #            #',
    r'####>>>######   ########>>>###',
    r'#           #   #            #',
    r'#           #>>>#            #',
    r'#     * #     @     # *      #',
    r'#       #     K     #        #',
    r'##############################']
)

levels.append(
   [r'           ******             ',
    r'         /#########\          ',
    r'        /    @@     \         ',
    r'       /             \        ',
    r'    * />>>>>>>>>>>>>>>\ *     ',
    r'              K               ',
    r'                              ',
    r'   /                     \    ',
    r'                              ',
    r'                              ',
    r'                              ',
    r'                              ',
    r'                              ',
    r'                              ',
    r'      p                       ']
)

levels.append(
   [r'         ###########          ',
    r'         #    @    #          ',
    r'         #         #          ',
    r'    *                   *     ',
    r'      @  #         #  @       ',
    r'         #  *   *  #          ',
    r'   #######         #######    ',
    r'                              ',
    r'                              ',
    r'        #     *     #         ',
    r'   *    #  @    @   #         ',
    r'####\   #############   /#####',
    r'     \  *              /      ',
    r'      \       p       /  *    ',
    r'       ###############        ']
)

class Game():
  def __init__(self) -> None:
    turtle.setup(1000, 700) 
    self.level_index = 0
    self.cur_level = None
    self.bt1_next_level = self.new_button(10, 10, 'Уровень', self.load_level)
    self.btn_exit = self.new_button(10, 50, 'Выход', self.exit)

  @staticmethod    # Это означает, что метод не будет принимать экземпляр класса
  def new_button(x, y, caption: str = 'Кнопка', handler: callable = lambda x,y: None):
    scr = turtle.getscreen()
    canvas = scr.getcanvas()
    button = Button(canvas.master, text=caption, command=handler, font=('Arial', 10, 'bold'))
    button.pack()
    # Tkinter отмеряет координаты из левого верхнего угла.
    # Сместим на центр и перевернём кооринату у
    # x = x + scr.window_width / 2 
    # y = -1 * (y + scr.window_height / 2)
    button.place(x=x, y=y)

  def load_level(self):
    if self.cur_level:
      self.cur_level.end()
      turtle.getscreen().clear()
      turtle.tracer(False)
      self.level_index += 1
      if self.level_index == len(levels): self.level_index = 0
    self.cur_level = Level(levels[self.level_index], sprites)
    self.cur_level.start()

  @staticmethod    # Это означает, что метод не будет принимать экземпляр класса
  def exit():
    bye()

Game()

done()
