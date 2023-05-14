from turtle import Turtle
from random import randint
from time import sleep

def create_square(col):
    t = Turtle()
    t.color(col)
    t.shape('square')
    # t.shape('turtle')
    t.right(90)
    t.penup()
    t.hideturtle()
    return t

t1 = create_square('steel blue')
t2 = create_square('green')

border = Turtle()
border.color('red')
border.penup()
border.goto(-150,-150)
border.pendown()
border.hideturtle()
border.goto(150,-150)


def start():
  t1.hideturtle()
  t2.hideturtle()
  t1.goto(randint(-150,150),randint(0,170))
  t2.goto(randint(-150,150),randint(0,170))
  t1.showturtle()
  t2.showturtle()
  while True:
    if move1(): break
    if move2(): break


def move1():
    if t1.ycor() > -140:
        t1.fd(randint(1,10))
        sleep(0.05)
        return False
    t1.write('Проигрыш')
    t1.hideturtle()
    return True

def move2():
    if t2.ycor() > -140:
        t2.fd(randint(1,10))
        sleep(0.05)
        return False
    t2.write('Проигрыш')
    t2.hideturtle()
    return True
    
def catch1(x, y):
  t1.goto(randint(-150,150),randint(0,170))

def catch2(x, y):
  t2.goto(randint(-150,150),randint(0,170))
  
t1.onclick(catch1)
t2.onclick(catch2)

start()
