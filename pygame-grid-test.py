import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
import time
from random import choice
import numpy

# class Map(object):
#   def __init__(self,x,y): #matrix with x columns and y rows
#       self.Matrix = numpy.empty(x,y)

class Wall(object):
    is_blockable = True
    def __init__(self):
        pass
        
class player(object):
    def __init__(self):
        pass

class DungeonModel(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.Grid = numpy.zeros((x,y))
        print self.Grid
        for i in range(x):
            for j in range(y):
                if i == 0 or i == x-1 or j == 0 or j == y-1:
                    self.Grid[i,j] = 1
                else:
                    self.Grid[i,j] = choice([0,1])
    def __str__(self):
        return str(self.Grid)




class DungeonModelView(object):
    def __init__(self, model, screen, size):
        self.model = model
        self.screen = screen
        self.size = size

    def draw(self):
        for x in range(self.model.x):
            for y in range(self.model.y):
                if self.model.Grid[x,y] == 1:
                    r = pygame.Rect(x * self.size[1]/float(self.model.y), y * self.size[1]/float(self.model.y), self.size[1]/float(self.model.y), self.size[1]/float(self.model.y))
                    pygame.draw.rect(self.screen, pygame.Color('red'), r)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    size = (640, 480)
    screen = pygame.display.set_mode(size)
    model = DungeonModel(64,48)
    print model
    view = DungeonModelView(model, screen, size)
    # controller = PyGameMouseController(model)
    # controller = PyGameKeyboardController(model) 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running == False
                pygame.display.quit()
            # controller.handle_event(event)
        view.draw()
        time.sleep(.01)
