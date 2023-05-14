from turtle import *
from random import randint as rnd

t1 = Turtle()
t2 = Turtle()
t1.color('teal')
t2.color('red')
t1.penup()
t2.penup()
t1.goto(rnd(-200,200), rnd(-200,200))
t1.shape('turtle')
t1.points = 0
t2.points = 0

def catch1(x, y):
  t1.write(str(t1.points) + ' ой!', font=('', 10, 'normal'))
  t1.goto(rnd(-200,200), rnd(-200,200))
  t1.points += 1

def catch2(x, y):
  t2.write(str(t2.points) + ' ой!', font=('', 10, 'normal'))
  t2.goto(rnd(-200,200), rnd(-200,200))
  t2.points += 1

t1.onclick(catch1)
t2.onclick(catch2)
done()