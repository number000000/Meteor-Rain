import pygame
import random

pygame.init()

WIDTH = 600
HEIGHT = 600

FPS = 60
clock = pygame.time.Clock()

screen = pygame.display
screen = screen.set_mode((WIDTH, HEIGHT))
screen.fill((0, 0, 0))

yspeed = 2
xspeed = 2

class Star(object):
    def __init__(self, x, y, xspeed, yspeed):
        self.color = (255, 255, random.randint(130, 255))
        self.size = random.randint(1, 3)
        self.x = x
        self.y = y
        self.xspeed = xspeed
        self.yspeed = yspeed

    def move(self):
        if self.x >= WIDTH:
            self.x = 0
        if self.y >= HEIGHT:
            self.y = 0
        self.x += self.xspeed
        self.y += self.yspeed
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

stars = []

for i in range(50):
    x = random.randint(1, WIDTH - 1)
    y = random.randint(1, HEIGHT - 1)
    stars.append(Star(x, y, xspeed, yspeed))

lock = True

while lock:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lock = False

    screen.fill((0, 0, 0))

    for star in stars:
        star.draw()
        star.move()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()