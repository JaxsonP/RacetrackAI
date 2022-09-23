

from generateTrack import generateTrack
from car import Car, CarInput

import pygame
import time
import datetime
import random
import math

WIDTH = 6
HEIGHT = 5
SCALE = 100
N_CARS = 500
FRAME_RATE = 3

def main ():
  print("\n\n\n")
  
  # track gen
  print("Generating track... ", end="")
  track, start, checkpoints = generateTrack(WIDTH, HEIGHT, SCALE)
  track.save("track.png", format="PNG")

  start_orientation = start[1]
  start = start[0]
  print("Done")
  print([cp.toString() for cp in checkpoints])
  print(start_orientation)

  pygame.init()
  screen = pygame.display.set_mode([WIDTH * SCALE, HEIGHT * SCALE])

  # initializing cars
  Car.display_size = SCALE / 10
  Car.track = track
  Car.checkpoints = checkpoints
  Car.track_width = SCALE
  cars = []
  for i in range(N_CARS):
    print("Initializing " + str(i + 1) + " cars", end="\r")
    cars.append(Car(start.x, start.y, (math.pi / 2) - start_orientation * math.pi / 2))
  print()

  generations = 0
  last_display_frame = datetime.datetime.now()

  # main loop ------------------------------------------------------<<<<<<<<<<<<<<<<
  running = True
  print("Starting generation 0")
  generation_start_time = datetime.datetime.now()
  while running:
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    all_dead = True
    for car in cars:
      car.update()
      if car.dead == False:
        all_dead = False
    
    if all_dead: # >>>>>> the magic <<<<<<<
      generations += 1
      #print("All dead\nScoring cars")
      
      total_fitness = 0
      best_car = cars[0]
      for i in range(len(cars)):
        car = cars[i]

        # scoring the cars
        car.fitness = 100
        car.fitness += car.checkpoints_visited * 100
        car.fitness -= car.age / 30
        next_checkpoint = checkpoints[(car.checkpoint + 1) % len(checkpoints)]
        dist_to_checkpoint = math.dist((car.x, car.y), (next_checkpoint.x, next_checkpoint.y)) / SCALE
        car.fitness -= dist_to_checkpoint * 25
        car.fitness = car.fitness**6 / 1000

        car.aggregate_fitness = total_fitness + car.fitness
        total_fitness += car.fitness

        if car.fitness > best_car.fitness:
          best_car = car

      # finding best car

      # making new cars
      next_gen_inputs = []
      for i in range(N_CARS):
        
        new_inputs = []

        # selecting parent
        parent = None
        r = random.random() * total_fitness
        for car in cars:
          if r < car.aggregate_fitness:
            parent = car
            break
        # gene inheritance
        new_inputs = [CarInput(input.steering, input.acceleration) for input in parent.inputs]
        
        Car.mutate(new_inputs)
        
        next_gen_inputs.append(new_inputs)

      next_gen_inputs[0] = best_car.inputs
      
      # resetting cars
      for i in range(len(cars)):
        car = cars[i]
        car.dead = False

        car.x, car.y, car.rotation = start.x, start.y, (math.pi / 2) - start_orientation * math.pi / 2

        car.vel_x = 0
        car.vel_y = 0
        car.steer = 0

        car.age = 0
        car.inputs = next_gen_inputs[i]

        car.checkpoint = 0
        car.checkpoints_visited = 0
        car.fitness = 0
        car.aggregate_fitness = 0
      
      duration = round((datetime.datetime.now() - generation_start_time).microseconds / 1000)
      print(f"Completed generation {generations} ({duration}ms)")
      generation_start_time = datetime.datetime.now()



    # drawing <<<<
    if datetime.datetime.now() - last_display_frame > datetime.timedelta(seconds=1/FRAME_RATE):
      screen.fill((200, 217, 111))
      track_image = pygame.image.load("track.png")
      track_image.set_colorkey((0), pygame.RLEACCEL)
      screen.blit(track_image, track_image.get_rect())

      #for cp in checkpoints:
        #pygame.draw.circle(screen, (200, 200, 200), (cp.x, cp.y), Car.track_width / 2, 3)

      for i in range(len(cars)):
        if i == 0:
          pygame.draw.circle(screen, (0, 0, 0), (cars[i].x, cars[i].y), SCALE / 4, 2)
        cars[i].draw(screen)

      pygame.display.flip()

      last_display_frame = datetime.datetime.now()

  pygame.quit()

  return 1



if __name__ == "__main__":
  main()
