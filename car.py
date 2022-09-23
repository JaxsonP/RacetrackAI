
from math import cos, sin, atan, sqrt, pi, dist
import pygame
import random

class CarInput:

  def __init__(self, steering=0, acceleration=1):
    self.steering = steering
    self.acceleration = acceleration
  
  def random ():
    new = CarInput()
    new.steering = (random.random() * Car.turn_speed * 2) - Car.turn_speed
    new.acceleration = 1#random.choice((-1, 0, 1))
    return new


class Car:

  # static display vars
  display_size = 100
  car_radius = None
  corner_angle = None
  color = pygame.Color(196, 71, 69)

  # static mechanics vars
  max_speed = 4
  max_turn = 0.05

  acceleration_speed = 0.15
  brake_speed = 0.08
  turn_speed = 0.1#0.005

  # misc
  track = None
  checkpoints = []
  track_width = 0



  def __init__(self, x_pos, y_pos, init_rotation):

    self.x = x_pos
    self.y = y_pos
    self.rotation = init_rotation

    self.vel_x = 0
    self.vel_y = 0
    self.steer = 0

    if Car.car_radius == None:
      Car.car_radius = sqrt(5) * Car.display_size / 2
      Car.corner_angle = atan(0.5)
    
    self.age = 0
    self.inputs = []
    self.inputs.append(CarInput())

    self.dead = False

    self.checkpoint = 0
    self.checkpoints_visited = 0
    self.fitness = 0
    self.aggregate_fitness = 0

    

  def update(self):

    if self.dead:
      return

    #  ----- mechanics
    self.x += self.vel_x
    self.y += self.vel_y
    self.rotation += self.inputs[self.age].steering#self.steer

    vel_magnitude = sqrt(self.vel_x**2 + self.vel_y**2)

    # applying car inputs
    if self.inputs[self.age].acceleration == 1:
      self.vel_x += cos(self.rotation) * Car.acceleration_speed
      self.vel_y += sin(self.rotation) * Car.acceleration_speed
    elif self.inputs[self.age].acceleration == -1 and vel_magnitude > 0.25:
      self.vel_x -= cos(self.rotation) * Car.brake_speed
      self.vel_y -= sin(self.rotation) * Car.brake_speed
    else:
      pass
    
    self.steer += self.inputs[self.age].steering
    
    # limiting speed
    vel_magnitude = sqrt(self.vel_x**2 + self.vel_y**2)
    if vel_magnitude > Car.max_speed:
      self.vel_x = self.vel_x / vel_magnitude * Car.max_speed
      self.vel_y = self.vel_y / vel_magnitude * Car.max_speed

    elif vel_magnitude < 0:
      self.vel_x = 0
      self.vel_y = 0
    #print(round(vel_magnitude, 4))
    #print(round(self.vel_x, 2)," : ",round(self.vel_y, 2))

    #limiting turn
    if self.steer > Car.max_turn:
      self.steer = Car.max_turn
    elif self.steer < -Car.max_turn:
      self.steer = -Car.max_turn

    # verifying on track
    if Car.track.getpixel((round(self.x), round(self.y))) == 0:
      self.die()
      pass

    # checkpoints
    for i in range(len(Car.checkpoints)):
      if dist((self.x, self.y), (Car.checkpoints[i].x, Car.checkpoints[i].y)) < Car.track_width / 2:
        #print(i)
        if i == self.checkpoint + 1 or (i == 0 and self.checkpoint == len(Car.checkpoints) - 1):
          self.checkpoint = i
          self.checkpoints_visited += 1
        elif i != self.checkpoint:
          #print("went backwards")
          self.die()
        break
    
    self.age += 1

    if self.age >= len(self.inputs):
      self.inputs.append(CarInput.random())


  

  def draw(self, surface):

    # drawing
    a = Car.corner_angle
    c = Car.car_radius
    r = self.rotation
    pygame.draw.polygon(surface, Car.color, [(self.x+cos(r+a)*c, self.y+sin(r+a)*c), (self.x+cos(r+pi-a)*c, self.y+sin(r+pi-a)*c), (self.x+cos(r+pi+a)*c, self.y+sin(r+pi+a)*c), (self.x+cos(r-a)*c, self.y+sin(r-a)*c)], 0)
    pygame.draw.polygon(surface, (50, 50, 50), [(self.x+cos(r)*c, self.y+sin(r)*c), (self.x+cos(r+pi-a)*c, self.y+sin(r+pi-a)*c), (self.x+cos(r+pi+a)*c, self.y+sin(r+pi+a)*c)], 0) 


  def die(self):
    #print(self.checkpoints_visited)
    self.dead = True

  def mutate(inputs):

    for i in range(len(inputs)):
      new_input = CarInput()
      r = random.random()
      if r < 0.001:
        inputs[i].steering = (random.random() * Car.turn_speed * 2) - Car.turn_speed
      elif r < 0.1 and len(inputs) - i < 60:
        inputs[i].steering = (random.random() * Car.turn_speed * 2) - Car.turn_speed


#(self.x+cos(r+a)*c, self.y+sin(r+a)*c), 