#!/usr/bin/env python

import os
import os.path
import sys
import pygame
from pygame.locals import *
import time
import random
from mpi4py import MPI
from pygame import mixer
import pygame.freetype

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

class Star(object):
    color = (0, 0, 0)
    x = 0
    y = 0
    size = 1
    xspeed = 1
    yspeed = 1

    def __init__(self, x, y, xspeed, yspeed):
        self.color = (255, 255, random.randint(130, 255))
        self.size = random.randint(1, 7)
        self.x = x
        self.y = y
        self.xspeed = xspeed
        self.yspeed = yspeed

    def move(self):
        if self.x >= (width * 2):
            self.x = 0
        if self.y >= (height * 2):
            self.y = 0
        self.x += self.xspeed
        self.y += self.yspeed

    def draw(self, screen, offset_x, offset_y):
        pygame.draw.circle(screen, self.color, (self.x - offset_x, self.y - offset_y), self.size, 0)


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
#thing = Thing(universe_size, int(width/2), int(height/2), (0,0,0), 0, 0)
yspeed = 20
xspeed = 12
stars = []
for i in range(80):
    x = random.randint(1, (width - 1) * 2)
    y = random.randint(1, (height - 1) * 2)
    stars.append(Star(x, y, xspeed, yspeed))

# set up the screen
screen = pygame.display.set_mode((screen_size), pygame.NOFRAME)

#Load images
bg_image1 = pygame.image.load('sky001.jpg')
bg_image1 = pygame.transform.scale(bg_image1, (width, height))
bg_image2 = pygame.image.load('sky002.jpg')
bg_image2 = pygame.transform.scale(bg_image2, (width, height))
bg_image3 = pygame.image.load('sky003.jpg')
bg_image3 = pygame.transform.scale(bg_image3, (width, height))
bg_image4 = pygame.image.load('sky004.jpg')
bg_image4 = pygame.transform.scale(bg_image4, (width, height))

#music set up
if rank == 0:
    mixer.init()
    mixer.music.load('skyMusic.mp3')
    print("music started playing")
    mixer.music.set_volume(0.2)
    mixer.music.play()

#Text
GAME_FONT = pygame.freetype.Font("moveon.ttf", 24)
text_surface, rect = GAME_FONT.render('Meteor Rain', (255, 255, 255))

# this is a function that will run the red dot
def run_it(stars):
    #for star in stars:
    #calculate rectangle steps and dimensions
    #color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    #speed = random.randint(4, 30)
    #size = random.randint(20,200)
    #thing.set_color(color) # the only difference is a new color per run 
    #thing.set_speed(speed)
    #thing.set_size(size)
    #calculate rectangle steps and dimensions
    #xer = int(width / thing.get_speed())
    #yer = int(height / thing.get_speed())
    #steps = (xer + yer) * 2
    # animate
    #for k in range(steps): # for drawing a screen sized rectangle
        comm.Barrier() # synchronization between all nodes
        if rank == 0:
            screen.fill((255, 255, 255))
            screen.blit(bg_image1, (0, 0))
            """
            if k < xer:
                thing.right()
            elif k < (xer + yer):
                thing.down()
            elif k < (xer * 2 + yer):
                 thing.left()
            else: # k < (xer + yer) * 2
                 thing.up()
            """
            for star in stars:
                star.move()
                comm.bcast(star, root=0)
                #thing.tell_me()
                star.draw(screen, 0, 0)
            screen.blit(text_surface, (10,10))
            GAME_FONT.render_to(screen, (10, 40), "by Meihui Liu", (255, 255, 255))
        elif rank == 1:
            screen.fill((0, 0, 0))
            screen.blit(bg_image2, (0, 0))
            for star in stars:
                star = comm.bcast(star, root=0)
                #thing.tell_me()
                star.draw(screen, width, 0)
            screen.blit(text_surface, (10,10))
            GAME_FONT.render_to(screen, (10, 40), "by Meihui Liu", (255, 255, 255))
        elif rank == 2:
            screen.fill((0, 0, 0))
            screen.blit(bg_image3, (0, 0))
            for star in stars:
                star = comm.bcast(star, root=0)
                star.draw(screen, 0, height)
            screen.blit(text_surface, (10,10))
            GAME_FONT.render_to(screen, (10, 40), "by Meihui Liu", (255, 255, 255))
        else:      #rank == 3:
            screen.fill((0, 0, 0))
            screen.blit(bg_image4, (0, 0))
            for star in stars:
                star = comm.bcast(star, root=0)
                star.draw(screen, width, height)
            screen.blit(text_surface, (10,10))
            GAME_FONT.render_to(screen, (10, 40), "by Meihui Liu", (255, 255, 255))
        pygame.display.update()
        clock.tick(60)

while True:
    run_it(stars)