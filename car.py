
from cmath import cos
import pygame
import math
import random

class CarInput:

  def __init__(self):
    self.steering = 0
    self.acceleration = 0
  
  def random ():
    new = CarInput()
    new.steering = 0#Car.turn_speed#(random.random() * Car.turn_speed * 2) - Car.turn_speed
    new.acceleration = 1#random.choice([-1, 0, 1])
    return new


class Car:

  # static display vars
  display_size = 100
  car_radius = None
  corner_angle = None
  color = pygame.Color(196, 71, 69)

  # static mechanics vars
  max_speed = 3
  max_turn = 0.1

  acceleration_speed = 0.05
  brake_speed = 0.08
  turn_speed = 0.01

  # misc
  track = None



  def __init__(self, x_pos, y_pos, init_rotation):

    self.x = x_pos
    self.y = y_pos
    self.rotation = init_rotation

    self.vel_x = 0
    self.vel_y = 0
    self.steer = 0

    if Car.car_radius == None:
      Car.car_radius = math.sqrt(5) * Car.display_size / 2
      Car.corner_angle = math.atan(0.5)
    
    self.age = 0
    self.inputs = []
    self.inputs.append(CarInput.random())

    self.dead = False

    

  def update(self):

    if self.dead:
      return

    #  ----- mechanics
    self.x += self.vel_x
    self.y += self.vel_y
    self.rotation += self.steer

    # applying car inputs
    if self.inputs[self.age].acceleration == 1:
      self.vel_x += math.cos(self.rotation) * Car.acceleration_speed
      self.vel_y += math.sin(self.rotation) * Car.acceleration_speed
    elif self.inputs[self.age].acceleration == -1:
      self.vel_x -= math.cos(self.rotation) * Car.brake_speed
      self.vel_y -= math.sin(self.rotation) * Car.brake_speed
    else:
      pass
    
    self.steer += self.inputs[self.age].steering

    if Car.track.getpixel((self.x, self.y)) == 0:
      #self.die()
      pass

    
    # limiting speed
    vel_magnitude = math.sqrt(self.vel_x**2 + self.vel_y**2)
    if vel_magnitude > Car.max_speed:
      self.vel_x = self.vel_x / vel_magnitude * Car.max_speed
      self.vel_y = self.vel_y / vel_magnitude * Car.max_speed

    elif vel_magnitude < 0:
      self.vel_x = 0
      self.vel_y = 0

    #limiting turn
    if self.steer > Car.max_turn:
      self.steer = Car.max_turn
    elif self.steer < -Car.max_turn:
      self.steer = -Car.max_turn

    
    self.age += 1

    if self.age >= len(self.inputs):
      self.inputs.append(CarInput.random())


  

  def draw(self, surface):

    # drawing
    a = Car.corner_angle
    c = Car.car_radius
    r = self.rotation
    pygame.draw.polygon(surface, Car.color, [(self.x+math.cos(r+a)*c, self.y+math.sin(r+a)*c), (self.x+math.cos(r+math.pi-a)*c, self.y+math.sin(r+math.pi-a)*c), (self.x+math.cos(r+math.pi+a)*c, self.y+math.sin(r+math.pi+a)*c), (self.x+math.cos(r-a)*c, self.y+math.sin(r-a)*c)], 0)
    #pygame.draw.polygon(surface, Car.color, [(self.x+math.cos(r)*c, self.y+math.sin(r+a)*c), (self.x+math.cos(r+math.pi-a)*c, self.y+math.sin(r+math.pi-a)*c), (self.x+math.cos(r+math.pi+a)*c, self.y+math.sin(r+math.pi+a)*c), (self.x+math.cos(r-a)*c, self.y+math.sin(r-a)*c)], 0) 
  

  def die(self):
    self.dead = True


#(self.x+math.cos(r+a)*c, self.y+math.sin(r+a)*c), 