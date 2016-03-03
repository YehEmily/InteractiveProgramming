import pygame
from pygame import *
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
import time
from random import choice, randint
import numpy

# class Map(object):
#   def __init__(self,x,y): #matrix with x columns and y rows
#       self.Matrix = numpy.empty(x,y)

class Wall(object):
    is_blockable = True
    def __init__(self):
        pass

def clearRectangle(grid, gridx, gridy, left, top, width, height): #grid is an array, gridx is the largest rightward index 1 is walls, 0 is empty space
    if left + width > gridx:
        rightbound = gridx
    else:
        rightbound = left + width
    if top - height < 0:
        upperbound = 0
    else:
        upperbound = top - height
    for i in range(left,rightbound):
        for j in range(upperbound,top):
            grid[i,j] = 0
        
def generate_rectangles(player, minRec, maxRec, grid, gridx, gridy, maxwidth, maxheight):
    total_rec = randint(minRec, maxRec)
    for i in range(total_rec):
        if i == 0: #make sure a 3x3 is always around the player.
            clearRectangle(grid, gridx, gridy, player.xpos-1, player.ypos+2, 3, 3)
        width = randint(int(maxwidth/float(2)), maxwidth)
        height = randint(int(maxheight/float(2)), maxheight)
        randx = randint(1,gridx-1)
        randy = randint(1, gridy-1) #random coordinate
        clearRectangle(grid, gridx, gridy, randx, randy, width, height)


class Player(object):
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.history = (xpos+1,ypos+1)

class Monster(object):
    def __init__(self, player, grid, xposition=20, yposition=20):
        self.xpos = xposition 
        self.ypos = yposition
        self.player = player
        self.history = (xposition+1, yposition+1)
        self.grid = grid

    def move(self, grid, speed=1):
        self.history = (self.xpos,self.ypos)
        if self.xpos > self.player.xpos and self.grid[self.xpos-1,self.ypos] != 1:
            self.xpos -= speed
        elif self.xpos < self.player.xpos and self.grid[self.xpos+1,self.ypos] != 1:
            self.xpos += speed

        elif self.ypos > self.player.ypos and self.grid[self.xpos,self.ypos-1] != 1:
            self.ypos -= speed
        elif self.ypos < self.player.ypos and self.grid[self.xpos,self.ypos+1] != 1:
            self.ypos += speed

class DungeonModel(object):
    def __init__(self, x, y, xpos, ypos):
        self.x = x
        self.y = y
        self.Grid = numpy.ones((x,y))
        self.Player = Player(xpos,ypos)
        self.Monster = Monster(self.Player, self.Grid)
        # print self.Grid
        generate_rectangles(self.Player, 5, 8, self.Grid, self.x, self.y, 40, 40)
        # self.Grid[0, :] = self.Grid[-1, :] = 1
        # self.Grid[:, 0] = self.Grid[:, -1] = 1

        # for i in range(x):
        #     for j in range(y):
        #         if i == 0 or i == x-1 or j == 0 or j == y-1:
        #             self.Grid[i,j] = 1
                # else:
                #     self.Grid[i,j] = choice([0,1])
    def __str__(self):
        return str(self.Grid)

class PyGameKeyboardController(object):
    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        """ Look for left and right keypresses to
            modify the x position of the paddle """
        if event.type != KEYDOWN:
            return
   #    while running:
   #        keys = pygame.key.get_pressed()
   #        if keys[pygame.K_LEFT] and self.model.Player.xpos > 1:
   #            self.model.Player.xpos -= 1
            # if keys[pygame.K_RIGHT] and self.model.Player.xpos < self.model.x - 1:
            #   self.model.Player.xpos += 1
            # if keys[pygame.K_UP] and self.model.Player.ypos > 1:
            #   self.model.Player.ypos -=1
            # if keys[pygame.K_DOWN] and self.model.Player.ypos < self.model.y - 1:
            #   self.model.Player.ypos +=1
        self.model.Player.history = (self.model.Player.xpos,self.model.Player.ypos)
        if event.key == pygame.K_LEFT and self.model.Grid[self.model.Player.xpos-1,self.model.Player.ypos] == 0:
            self.model.Player.xpos -= 1
        elif event.key == pygame.K_RIGHT and self.model.Grid[self.model.Player.xpos+1,self.model.Player.ypos] == 0:
            self.model.Player.xpos += 1
        elif event.key == pygame.K_UP and self.model.Grid[self.model.Player.xpos,self.model.Player.ypos-1] == 0:
            self.model.Player.ypos -=1
        elif event.key == pygame.K_DOWN and self.model.Grid[self.model.Player.xpos,self.model.Player.ypos+1] == 0:
            self.model.Player.ypos +=1
        
        self.model.Monster.move(self.model.Monster.grid)


class DungeonModelView(object):
    def __init__(self, model, screen, size):
        self.model = model
        self.screen = screen
        self.size = size

    def drawMap(self):
        self.screen.fill(pygame.Color('black'))
        for x in range(self.model.x):
            for y in range(self.model.y):
                if self.model.Grid[x,y] == 1:
                    r = pygame.Rect(x * self.size[1]/float(self.model.y), y * self.size[1]/float(self.model.y), self.size[1]/float(self.model.y), self.size[1]/float(self.model.y))
                    pygame.draw.rect(self.screen, pygame.Color('red'), r)

        pygame.display.update()

    def drawPlayer(self):
        p = pygame.Rect(self.model.Player.xpos * self.size[1]/float(self.model.y), self.model.Player.ypos * self.size[1]/float(self.model.y), self.size[1]/float(self.model.y), self.size[1]/float(self.model.y))
        pygame.draw.rect(self.screen, pygame.Color('white'), p)
        if self.model.Player.xpos != self.model.Player.history[0] or self.model.Player.ypos != self.model.Player.history[1]:
            b = pygame.Rect(self.model.Player.history[0] * self.size[1]/float(self.model.y), self.model.Player.history[1] * self.size[1]/float(self.model.y), self.size[1]/float(self.model.y), self.size[1]/float(self.model.y))
            pygame.draw.rect(self.screen, pygame.Color('black'), b)
        pygame.display.update()

    def drawMonster(self):
        p = pygame.Rect(self.model.Monster.xpos * self.size[1]/float(self.model.y), self.model.Monster.ypos * self.size[1]/float(self.model.y), self.size[1]/float(self.model.y), self.size[1]/float(self.model.y))
        pygame.draw.rect(self.screen, pygame.Color('green'), p)
        if self.model.Monster.xpos != self.model.Monster.history[0] or self.model.Monster.ypos != self.model.Monster.history[1]:
            b = pygame.Rect(self.model.Monster.history[0] * self.size[1]/float(self.model.y), self.model.Monster.history[1] * self.size[1]/float(self.model.y), self.size[1]/float(self.model.y), self.size[1]/float(self.model.y))
            pygame.draw.rect(self.screen, pygame.Color('black'), b)
        pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    screenX = 1080
    screenY = 720
    size = (screenX, screenY)
    screen = pygame.display.set_mode(size)
    model = DungeonModel(int(screenX/float(10)),int(screenY/float(10)),2,2)
    print model
    view = DungeonModelView(model, screen, size)
    # controller = PyGameMouseController(model)
    controller = PyGameKeyboardController(model) 
    running = True
    view.drawMap()
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running == False
                pygame.display.quit()
            controller.handle_event(event)
        view.drawPlayer()
        view.drawMonster()
        time.sleep(.01)
