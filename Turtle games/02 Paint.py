from turtle import *


v = 0 #максимальная скорость черепашки
step = 15 #шаг

t = Turtle()
t.color('blue')
t.width(5)
t.shape('circle')
t.pendown()
t.speed(v)
t.i = 0

def draw(x, y):
  t.goto(x, y)


def move(x, y):
  t.penup()
  t.goto(x, y)
  t.pendown()


def stepspace():
  c = ['indian red', 'white', 'green', 'purple', 'yellow', 'steel blue', 'pink']
  t.color(c[t.i])
  t.i += 1
  if t.i > 6:
    t.i = 0


def stepUp():
 t.goto(t.xcor(), t.ycor() + step)


def stepDown():
 t.goto(t.xcor(), t.ycor() - step)


def stepLeft():
 t.goto(t.xcor() - step, t.ycor())


def stepRight():
 t.goto(t.xcor() + step, t.ycor())


def startFill():
  t.begin_fill()


def endFill():
  t.end_fill()

def sizepen_1():
  t.width(1)
  
def sizepen_2():
  t.width(5)

def sizepen_2():
  t.undo()
  
t.ondrag(draw)


scr = t.getscreen()
scr.onscreenclick(move)
scr.onkey(stepspace,'space')
scr.onkey(stepUp,'Up')
scr.onkey(stepDown,'Down')
scr.onkey(stepLeft,'Left')
scr.onkey(stepRight,'Right')
scr.onkey(startFill,'f')
scr.onkey(endFill,'e')
scr.onkey(sizepen_1, 'w')
scr.onkey(sizepen_2, 's')


scr.listen()
done()