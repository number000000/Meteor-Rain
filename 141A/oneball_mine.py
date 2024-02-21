import os
import os.path
import sys
import pygame
from pygame.locals import *
import time
import random
from mpi4py import MPI

# simple thing that can move around
class Thing:
    x = 0 # x and y are relative to the whole coord system
    y = 0
    speed = 1
    universe_size = (0,0)
    color = (255, 0, 0)

    def __init__(self, universe_size, x, y, color, size, speed):
        self.universe_size = universe_size
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.speed = speed

    def draw(self, screen, offset_x, offset_y):
        pygame.draw.circle(screen, self.color, \
               (self.x-offset_x,self.y-offset_y), self.size, 0)

    # tell_me is here for testing
    def tell_me(self):
        print(rank, self.x, self.y, self.color, self.size, self.speed)

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def set_speed(self, speed):
        self.speed = speed

    def get_speed(self):
        return self.speed

    def set_size(self, size):
        self.size = size

    def get_size(self, size):
        return size

    def up(self):
        self.y = self.y - self.speed

    def down(self):
        self.y = self.y + self.speed

    def right(self):
        self.x = self.x + self.speed

    def left(self):
        self.x = self.x - self.speed

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# set window position
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
# get this display
os.environ['DISPLAY'] = ':0.0'
# with caffeine installed (sudo apt install caffeine) we can wake the screen
os.system('caffeinate sleep 1') # passes caffeinate out to shell to wake screensaver

# init clock and display
clock = pygame.time.Clock()
pygame.display.init()
pygame.mouse.set_visible(False)

# get the screen hight and width
disp_info = pygame.display.Info()
width = disp_info.current_w
height = disp_info.current_h
screen_size = (width,height)
universe_size = (width*2, height*2)

# make a thing
thing = Thing(universe_size, int(width/2), int(height/2), (0,0,0), 0, 0)

# set up the screen
screen = pygame.display.set_mode((screen_size), pygame.NOFRAME)

# this is a function that will run the red dot
def run_it(thing):
    #calculate rectangle steps and dimensions
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    speed = random.randint(4, 30)
    size = random.randint(20,200)
    thing.set_color(color) # the only difference is a new color per run
    thing.set_speed(speed)
    thing.set_size(size)
    #calculate rectangle steps and dimensions
    xer = int(width / thing.get_speed())
    yer = int(height / thing.get_speed())
    steps = (xer + yer) * 2
    # animate
    for k in range(steps): # for drawing a screen sized rectangle
        comm.Barrier() # synchronization between all nodes
        if rank == 0:
            screen.fill((255, 255, 255))
            if k < xer:
                thing.right()
            elif k < (xer + yer):
                thing.down()
            elif k < (xer * 2 + yer):
                 thing.left()
            else: # k < (xer + yer) * 2
                 thing.up()
            comm.bcast(thing, root=0)
            #thing.tell_me()
            thing.draw(screen, 0, 0)
        elif rank == 1:
            screen.fill((220,220,220))
            thing = comm.bcast(thing, root=0)
            #thing.tell_me()
            thing.draw(screen, width, 0)
        elif rank == 2:
            screen.fill((200,200,200))
            thing = comm.bcast(thing, root=0)
            thing.draw(screen, 0, height)
        else:      #rank == 3:
            screen.fill((180, 180, 180))
            thing = comm.bcast(thing, root=0)
            thing.draw(screen, width, height)
        pygame.display.update()
        clock.tick(30)

while True:
    run_it(thing)