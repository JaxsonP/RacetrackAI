
from generateTrack import generateTrack
from car import Car, CarInput

import pygame
import time
import random
import math

WIDTH = 6
HEIGHT = 5
SCALE = 100
N_CARS = 1

def main ():

  

  print("Generating track... ", end="")
  track, start = generateTrack(WIDTH, HEIGHT, SCALE)
  track.save("track.png", format="PNG")
  horizontal_start = start[1]
  start = start[0]
  print("Done")

  pygame.init()
  screen = pygame.display.set_mode([WIDTH * SCALE, HEIGHT * SCALE])

  Car.display_size = SCALE / 10
  Car.track = track
  cars = []
  for i in range(N_CARS):
    print("Initializing " + str(i) + " cars", end="\r")
    cars.append(Car(start.x * SCALE + SCALE / 2, start.y * SCALE + SCALE / 2, 0))


  def draw(screen):#233, 226, 230

    screen.fill((200, 217, 111))
    track_image = pygame.image.load("track.png")
    track_image.set_colorkey((0), pygame.RLEACCEL)
    screen.blit(track_image, track_image.get_rect())

    return 1
  


  running = True
  while running:
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    time.sleep(1/60)

    for car in cars:
      car.update()


    # drawing
    draw(screen)

    for car in cars:
      
      car.draw(screen)

    pygame.display.flip()

  pygame.quit()

  return 1



if __name__ == "__main__":
  main()
