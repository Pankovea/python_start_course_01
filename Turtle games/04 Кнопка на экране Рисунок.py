from turtle import Turtle, done, bye

t = Turtle()
t.color('red')
t.shape('circle')
t.pendown()
t.speed(0)
def draw(x, y):
  t.goto(x, y)
t.ondrag(draw)

scr = t.getscreen()
scr.btns_coord = [] # Здесь будут хрвниться координаты кнопок для проверки нажатия
def new_button(x, y, w, h, caption: str = 'Кнопка', handler: callable = lambda x,y: None):
  """Кнопка с надписью"""
  btn = Turtle()
  btn.hideturtle()
  btn.penup()
  btn.speed(0)
  btn.goto(x, y)
  btn.pendown()
  # рисуем прямоугольник
  for i in range(4):
      if i in [1,3]:
          btn.fd(h)
      else:
          btn.fd(w)
      btn.left(90)
  btn.penup()
  # перемещаем перо внутрь прямоугольника
  btn.goto(btn.xcor() + w/2, btn.ycor() + h/2 - 12)
  # выводим надпись
  btn.write(caption, align='center',font=("Arial", 12, "normal"))
  # Добавляем координаты кнопки
  scr.btns_coord.append((x, x+w, y, y+w, handler))
  return btn

def but_click(mx, my):
  '''Клик по кнопке
  проверяем попадают ли координаты 
  клика по холсту в координаты кнопки'''
  for coord in scr.btns_coord:
    if coord[0] < mx < coord[1] and coord[2] < my < coord[3]:
      coord[4]()
      break

scr.onclick(but_click)

def exit():
  bye()

def color():
  t.color('blue')

bt1 = new_button(-150, 250, 100, 30, 'Цвет', color)
bt2 = new_button(0, 250, 100, 30, 'Выход', exit)

done()