from turtle import *
from random import randint

s_width = 200
s_height = 180

class Sprite(Turtle):
   def __init__(self, x, y, shape, color):
       Turtle.__init__(self)
       self.penup()
       self.goto(x, y)
       self.color(color)
       self.shape(shape)
       self.left(180)
       self.step = 0
       self.points = 0


   def accelerate(self):
       self.step = self.step * 1.5 or self.step + 2
   def brk(self):
       self.step = self.step / 1.5 if self.step > 2 else 0
   def turn_to_left(self):
       self.left(30)
   def turn_to_right(self):
       self.right(30)
  
   def make_step(self):
       self.forward(self.step)

   def is_collide(self, sprite):
       dist = self.distance(sprite.xcor(), sprite.ycor())
       if dist < 20:
           return True
       else:
           return False

class Enemy(Sprite):
  def __init__(self, x, y, shape, color):
       super().__init__(x, y, shape, color)
       self.step=20
       self.speed(10)

       
  def move_target(self, x_start, y_start, x_end, y_end):
    self.x_start = x_start
    self.y_start = y_start       
    self.x_end = x_end
    self.y_end = y_end
    self.goto(x_start, y_start)
    self.setheading(self.towards(x_end, y_end)) 
  
  def make_step(self):
    self.forward(self.step) #направление уже есть
    if self.distance(self.x_end, self.y_end) < self.step: 
      self.move_target(self.x_end, self.y_end, self.x_start, self.y_start)


player = Sprite(170, 160, 'turtle', 'green')
enemy1 = Enemy(s_width, -90, 'triangle', 'red')
enemy1.move_target(s_width, -90, -s_width, -90)
enemy2 = Enemy(-s_width, 90, 'triangle', 'red')
enemy2.move_target(-s_width, 90, s_width, 90)
enemy3 = Enemy(-90, s_height, 'triangle', 'red')
enemy3.move_target(-90, s_height, -90, -s_height)
coin = Sprite(-170, -150, 'circle', 'yellow')


scr = player.getscreen()
scr.listen()
scr.onkey(player.accelerate, 'Up')
scr.onkey(player.turn_to_left, 'Left')
scr.onkey(player.turn_to_right, 'Right')
scr.onkey(player.brk, 'Down')


while player.points < 2:
  enemy1.make_step()
  enemy2.make_step()
  enemy3.make_step()
  player.make_step()


  if player.is_collide(coin):
    player.points += 1
    coin.goto(randint(-80, 80), randint(-80, 80))
    
  
  if player.is_collide(enemy1) \
  or player.is_collide(enemy2) \
  or player.is_collide(enemy3):
    coin.hideturtle()
    break


  if player.points == 2:
    enemy1.hideturtle()
    enemy2.hideturtle()
    enemy3.hideturtle()
