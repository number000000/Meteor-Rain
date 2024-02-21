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
        #pygame.draw.circle(screen, self.color, \
        #       (self.x-offset_x,self.y-offset_y), self.size, 0)
        pygame.draw.line(screen, self.color, \
                (self.x-offset_x, self.y-offset_y), \
               (self.x-offset_x-20, self.y-offset_y), width=5)

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

class Snake:
    def __init__(self):
        self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
        self.length = random.randint(2, width - int(width/3))
        self.size = random.randint(3, 6)
        self.heading = random.randint(0, 3)
        self.prev_heading = self.heading
        self.turning_points = []
        startPosX = random.randint(50, width-50) 
        startPosY = random.randint(50, height-50)
        if (self.heading == 0): # heading right
            endPosX = startPosX - self.length
            endPosY = startPosY
        if (self.heading == 1): # heading left
            endPosX = startPosX + self.length
            endPosY = startPosY
        if (self.heading == 2): # heading up
            endPosX = startPosX
            endPosY = startPosY + self.length
        if (self.heading == 3): # heading down
            endPosX = startPosX
            endPosY = startPosY - self.length
        self.turning_points.append((startPosX, startPosY))
        self.turning_points.append((endPosX, endPosY))
    
    def choose_turn_heading(self):
        self.prev_heading = self.heading
        up_down = [2, 3]
        left_right = [1, 0]
        startPosX = self.turning_points[0][0]
        startPosY = self.turning_points[0][1]
        if(self.prev_heading == 0 or self.prev_heading == 1):
            if(startPosY == 0): # at the top, can't go up
                self.heading = 3
            elif (startPosY == (height)): # at the bottom, can't got down
                self.heading = 2
            else:
                self.heading = random.choice(up_down)
        else:
            if(startPosX == 0): # at the left end, can't go left
                self.heading = 0
            elif (startPosX == (width)): # at the right end, can't go right
                self.heading = 1
            else: 
                self.heading = random.choice(left_right)
    
    def set_turning_point(self):
        turningPosX = self.turning_points[0][0]
        turningPosY = self.turning_points[0][1]
        self.turning_points.insert(1, (turningPosX, turningPosY))

    def turn(self):
        startPosX = self.turning_points[0][0]
        startPosY = self.turning_points[0][1]
        endPosX = self.turning_points[len(self.turning_points) - 1][0]
        endPosY = self.turning_points[len(self.turning_points) - 1][1]
        beforeEndX = self.turning_points[len(self.turning_points) - 2][0]
        beforeEndY = self.turning_points[len(self.turning_points) - 2][1]
            
        # checking if the first turn has ended
        if(endPosX == beforeEndX and endPosY == beforeEndY):
            self.turning_points.pop(len(self.turning_points) - 2) # remove the turning point cz the turn has ended
            beforeEndX = self.turning_points[len(self.turning_points) - 2][0] #get the new turning location
            beforeEndY = self.turning_points[len(self.turning_points) - 2][1]

        #move the snake
        if (self.heading == 0): # start is heading right
            startPosX += 1
        if (self.heading == 1): # start is heading left
            startPosX -= 1
        if (self.heading == 2): # start is heading up
            startPosY -= 1
        if (self.heading == 3): # start is heading down
            startPosY += 1
        if(endPosX == beforeEndX):
            if(endPosY > beforeEndY): #heading upward
                endPosY -= 1
            else: #heading downward
                endPosY += 1
        if(endPosY == beforeEndY):
            if(endPosX > beforeEndX): #heading left
                endPosX -= 1
            else: #heading right
                endPosX += 1
        #update start and end locations as snake has moved
        self.turning_points[0] = (startPosX, startPosY)
        self.turning_points[len(self.turning_points) - 1] = (endPosX, endPosY)
        #checking if we are done turning
        # print("endPosX " + str(self.endPosX) + " endPosY " + str(self.endPosY))
        # print("turningPosX " + str(self.turningPosX) + " turningPosY " + str(self.turningPosY))
        # print("startPosX " + str(self.startPosX) + " startPosY " + str(self.startPosY))
        
    def move(self):
        # print(self.turning_points)
        startPosX = self.turning_points[0][0]
        startPosY = self.turning_points[0][1]
        afterStartX = self.turning_points[1][0]
        afterStartY = self.turning_points[1][1]
        endPosX = self.turning_points[len(self.turning_points) - 1][0]
        endPosY = self.turning_points[len(self.turning_points) - 1][1]
        beforeEndX = self.turning_points[len(self.turning_points) - 2][0]
        beforeEndY = self.turning_points[len(self.turning_points) - 2][1]
            
        # checking if the first turn has ended
        if(endPosX == beforeEndX and endPosY == beforeEndY):
            self.turning_points.pop(len(self.turning_points) - 2) # remove the turning point cz the turn has ended
            beforeEndX = self.turning_points[len(self.turning_points) - 2][0] #get the new turning location
            beforeEndY = self.turning_points[len(self.turning_points) - 2][1]

        #move the snake
        if(startPosX == afterStartX):
            if(startPosY > afterStartY): #start is heading downward
                startPosY += 1
            else: #start is heading upward
                startPosY -= 1
        if(startPosY == afterStartY):
            if(startPosX > afterStartX): #start is heading right
                startPosX += 1
            else: #start is heading left
                startPosX -= 1
        if(endPosX == beforeEndX):
            if(endPosY > beforeEndY): #end is heading upward
                endPosY -= 1
            else: #end is heading downward
                endPosY += 1
        if(endPosY == beforeEndY):
            if(endPosX > beforeEndX): #end is heading left
                endPosX -= 1
            else: #end is heading right
                endPosX += 1
        #hit the edge
        if(startPosX == (width + 1) or startPosX == -1 \
            or startPosY == (height + 1) or startPosY == -1):
            self.choose_turn_heading()
            self.set_turning_point()
            self.turn()
            return
        #update start and end locations as snake has moved
        self.turning_points[0] = (startPosX, startPosY)
        self.turning_points[len(self.turning_points) - 1] = (endPosX, endPosY)

    def draw(self):
        p_turn = random.randint(0, 100)
        if(p_turn > 99):
            self.choose_turn_heading()
            self.set_turning_point()
            # print("CURRENT " + str(self.heading))
            # print("PREV " + str(self.prev_heading))
            self.turn()
        else:
            self.move()
        pygame.draw.lines(screen, self.color, False, self.turning_points, self.size)

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