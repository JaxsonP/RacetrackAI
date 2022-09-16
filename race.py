
from generateTrack import generateTrack

import pygame

WIDTH = 6
HEIGHT = 5
SCALE = 100

def main ():

  

  print("Generating track... ", end="")
  track, start = generateTrack(WIDTH, HEIGHT, SCALE)
  track.save("track.jpg", format="JPEG")
  horizontal_start = start[1]
  start = start[0]
  print("Done")

  return 1



if __name__ == "__main__":
  main()
