from sys import exit
import pygame
from pygame.locals import *
import random
#import pygame.freetype
#width = 3072
#height = 5440

width = 1000
height = 740

class Star(object):
    color = (0, 0, 0)
    x = 0
    y = 0
    size = 1
    xspeed = 1
    yspeed = 1

    def __init__(self, x, y, xspeed, yspeed):
        self.color = (255, 255, random.randint(130, 255))
        self.size = random.randint(1, 3)
        self.x = x
        self.y = y
        self.xspeed = xspeed
        self.yspeed = yspeed

    def move(self):
        if self.x >= width:
            self.x = 0
        if self.y >= height:
            self.y = 0
        self.x += self.xspeed
        self.y += self.yspeed

    def draw(self, screen, offset_x, offset_y):
        pygame.draw.circle(screen, self.color, (self.x - offset_x, self.y - offset_y), self.size, 0)

pygame.init()

# init clock and display
clock = pygame.time.Clock()
pygame.display.init()
pygame.mouse.set_visible(False)

# get the screen hight and width
screen_size = (width,height)

# make a thing
#thing = Thing(universe_size, int(width/2), int(height/2), (0,0,0), 0, 0)
yspeed = 3
xspeed = 1
stars = []
for i in range(80):
    x = random.randint(1, (width - 1))
    y = random.randint(1, (height - 1))
    stars.append(Star(x, y, xspeed, yspeed))

# set up the screen
screen = pygame.display.set_mode((screen_size))

#Load images
bg_image1 = pygame.image.load('./141A/blueNightFull.jpg')
bg_image1 = pygame.transform.scale(bg_image1, (width, height))

#Text
#font = pygame.font.Font(None, 32)
#text1 = font.render("Meteor Rain by Meihui Liu", True, (255, 255, 255))

# this is a function that will run the red dot
def run_it(stars):
    global frame_count
    screen.fill((255, 255, 255))
    screen.blit(bg_image1, (0, 0))
    for star in stars:
        star.move()
        star.draw(screen, 0, 0)
    #screen.blit(text1, (10,10))

    pygame.display.update()
    clock.tick(60)
    frame_count += 1
    filename = "./frames/frame_" + str(frame_count) + ".png"
    pygame.image.save(screen, filename)

lock = True
frame_count = 0
while lock:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lock = False
    run_it(stars)

pygame.quit()
exit()