from turtle import Turtle, done, bye
from tkinter import Button

t = Turtle()
t.color('red')
t.shape('circle')
t.pendown()
t.speed(0)
def draw(x, y):
  t.goto(x, y)
t.ondrag(draw)


def new_button(x, y, caption: str = 'Кнопка', handler: callable = lambda x,y: None):
  canvas = t.getscreen().getcanvas()
  button = Button(canvas.master, text=caption, command=handler, font=('Arial', 12, 'bold'))
  button.pack()
  button.place(x=x, y=y)  # Положение кнопки от левого верхнего угла


def exit():
  bye()

def color():
  t.color('blue')

bt1 = new_button(350, 20, 'Цвет', color)
bt2 = new_button(450, 20, 'Выход', exit)

done()