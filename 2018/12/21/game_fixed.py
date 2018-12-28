import pygame
import itertools
import sys
from pygame.locals import *


class PyManMain():
    def __init__(self, width = 640, height = 480):
        pygame.init()
        self.width = width
        self.height = height
        self.pellet_sprites = pygame.sprite.Group()
        self.screen = pygame.display.set_mode\
                      ((self.width , self.height))
    def LoadSprites(self):
        self.pacman = Pacman()
        self.sprites = pygame.sprite.Group()
        self.pellet_sprites = pygame.sprite.Group()
        self.sprites.add(self.pacman)
        # Создаем точки с помощью вложенных циклов for x/y in range(...):
        for x in range(10):
            for y in range(10):
                self.pellet_sprites.add((Pellet(pygame.Rect(x * 64, y * 64, 64, 64)))) # pygame.Rect(x, y, width, height)
    def MainLoop(self):
        self.LoadSprites()
        move = False
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0) # завершение работы программы с кодом 0 (без ошибки)
                elif event.type == KEYDOWN:
                    if event.key in (K_DOWN, K_UP, K_LEFT, K_RIGHT): # Pacman ходит по нажатию только клавиш-стрелок
                        move = True
                        key = event.key
                elif event.type == KEYUP:
                    if event.key in (K_DOWN, K_UP, K_LEFT, K_RIGHT): # Pacman останавливается по отпусканию только клавиш-стрелок (а не любой залипшей или случайно нажатой клавиши)
                        move = False
                        self.pacman.rotated = False
                elif event.type == 31: # перехватываем движения рта пакмана
                    self.pacman.next_costume()
            if move:
                self.pacman.move(key)        
            self.screen.fill((0,0,0))
            self.sprites.draw(self.screen)
            self.pellet_sprites.draw(self.screen)
            pygame.display.flip()
                    
class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pygame.time.set_timer(31, 150) # создаем событие изменения костюма с ID=31, которое потом обрабатываем
        self.costumes = itertools.cycle((pygame.image.load("images/pacman/yellow/open/medium.png"), pygame.image.load(r"images/pacman/yellow/close.png"))) # итер-объект, который возвращает то открытый, то закрытый рот
        self.image = pygame.image.load(r"images/pacman/yellow/open/medium.png")
        self.rect = self.image.get_rect()
        self.next_costume()
        self.vel = [0,0]
        self.rotated = False
        
    def move(self,key):
        if key == K_LEFT:
            self.vel[0] = -5
            self.vel[1] = 0
            if not self.rotated:
                self.costumes = itertools.cycle((pygame.transform.rotate(pygame.image.load("images/pacman/yellow/open/medium.png"), 90),
                                                 pygame.transform.rotate(pygame.image.load(r"images/pacman/yellow/close.png"), 90)))
                self.rotated = True # чтобы рот и дальше открывался и закрывался, меняем направление только 1 раз.

        elif key == K_UP:
            self.vel[1] = -5
            self.vel[0] = 0
            if not self.rotated:
                self.costumes = itertools.cycle((pygame.image.load("images/pacman/yellow/open/medium.png"),
                                                pygame.image.load(r"images/pacman/yellow/close.png")))
                self.rotated = True # чтобы рот и дальше открывался и закрывался, меняем направление только 1 раз.

        elif key == K_RIGHT:
            self.vel[0] = 5
            self.vel[1] = 0
            if not self.rotated:
                self.costumes = itertools.cycle((pygame.transform.rotate(pygame.image.load("images/pacman/yellow/open/medium.png"), -90),
                                                 pygame.transform.rotate(pygame.image.load(r"images/pacman/yellow/close.png"), -90)))
                self.rotated = True # чтобы рот и дальше открывался и закрывался, меняем направление только 1 раз.
                
        elif key == K_DOWN:
            self.vel[1] = 5
            self.vel[0] = 0
            if not self.rotated:
                self.costumes = itertools.cycle((pygame.transform.rotate(pygame.image.load("images/pacman/yellow/open/medium.png"), 180),
                                                 pygame.transform.rotate(pygame.image.load(r"images/pacman/yellow/close.png"), 180)))
                self.rotated = True # чтобы рот и дальше открывался и закрывался, меняем направление только 1 раз.
        pygame.time.wait(10)

        self.rect.left += self.vel[0]
        self.rect.top += self.vel[1]
        
    def next_costume(self):
        self.image = next(self.costumes)
        self.spos = (self.rect.top, self.rect.left)
        self.rect = self.image.get_rect()
        self.rect.top = self.spos[0]
        self.rect.left = self.spos[1]
        
class Pellet(pygame.sprite.Sprite):
    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/dot/medium.png')
        self.rect = self.image.get_rect()
        if rect != None:
            self.rect = rect
    

MainWindow = PyManMain()
MainWindow.MainLoop()
