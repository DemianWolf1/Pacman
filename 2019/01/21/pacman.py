import pygame
import itertools
import sys
from pygame.locals import *
from pygame.font import *
from walls import Walls

class Main():
    """ Main Pacman game class. """
    def __init__(self, width=640, height=550):
        self.width, self.height = (width, height) # creating self.width and self.height attributes
        pygame.init() # initializing pygame module
        self.play_sound("sound/beginning.wav") # plays intro sound
        pygame.time.set_timer(30, 4000) # timer to start the game
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN) # creating the game window (self.screen)
        pygame.display.set_caption("Python Pacman v.1.00dev0") # setting caption for the game window (using pygame.display.set_caption)
        self.walls = Walls.createList(Walls()) # creating list of walls' rectangulars (self.walls)
        self.background = pygame.image.load("images/bg.png") # creating background image (self.background)
        self.load_sprites() # load sprites for game
        self.move = False # while playing intro Pacman doesn't move
        self.key = K_RIGHT # when intro sound stops, Pacman goes right
        
    def load_sprites(self):
        """ Loads sprites for game. """
        self.pacman = Pacman(self) # creating Pacman object (self.pacman)
        self.pellet_sprites = pygame.sprite.Group() # creating pellet sprites' group (self.pellet_sprites)
        self.sprites = pygame.sprite.Group(self.pacman) # creating sprites' group (self.sprites)
        # Creating pellets using inserted for-loops
        for x in range(25): # pellets' x
            for y in range(25): # pellets' y
                cur_pellet = Pellet(pygame.Rect(x * 64, y * 64 + 60, 10, 10)) # current pellet object (cur_pellet)
                self.pellet_sprites.add(cur_pellet) # adding current pellet to the pellets' spritelist
                if cur_pellet.rect.left in range(100, 551) and cur_pellet.rect.top in range(50, 550) and \
                   not ((cur_pellet.rect.left in range(470, 550) or cur_pellet.rect.left in range(100, 180)) and cur_pellet.rect.top in range(300, 360)): # check if the position is good for the pellet
                    for wall in self.walls: # checking every wall using loop cycle
                        if wall.colliderect((cur_pellet.rect.left, cur_pellet.rect.top, cur_pellet.image.get_width(), cur_pellet.image.get_height())): # checking if current pellet collides any wall
                            cur_pellet.kill() # if yes, we must kill it!                 
                else:
                    cur_pellet.kill() # if not, we must kill it!

    def play_sound(self, filename):
        """ Plays sounds, specified as filename. """
        pygame.mixer.music.load(filename) # loads file by its filename,
        pygame.mixer.music.play() # and then plays it
                        
    def mainloop(self):
        """ Main loop of the game. """
        while True: # this loop mustn't stop until all the app stops!
            for event in pygame.event.get(): # we check every event...
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): # if we have got QUIT event or ESC is pressed,
                    pygame.quit() # we must uninitialize (quit) the pygame,
                    sys.exit(0) # and then exit the app at all (0 is exit code, if it's non-null, app failed)
                elif event.type == KEYDOWN: # if key is down,
                    if event.key in (K_DOWN, K_UP, K_LEFT, K_RIGHT): # Pacman goes only when you press DOWN/UP/LEFT/RIGHT arrow key
                        self.move = True # allow move!
                        self.key = event.key # save key code
                        self.pacman.rotated = False # pacman is not rotated
                        self.pacman.move(self.key) # move pacman
                elif event.type == 31: # if it's time to open/close Pacman's mouth, then
                    self.pacman.next_costume() # we must do it...
                elif event.type == 30: # if it's time to stop the intro sound and start the game,
                    self.move = True # allow Pacman move
                    pygame.time.set_timer(30, 0) # disable start game timer (because it will start every 4 seconds otherwise)
            self.screen.fill([0, 0, 0]) # fill screen with black color
            # checking if Pacman sprite collides with any wall
            for wall in self.walls: # checking every wall using loop cycle
                if wall.colliderect((self.pacman.rect.left + self.pacman.vel[0], self.pacman.rect.top + self.pacman.vel[1],\
                                     self.pacman.image.get_width(), self.pacman.image.get_height())): # checking if Pacman collides any wall
                    self.move = False # deny any move!
                    self.pacman.rect.left -= self.pacman.vel[0] # go back for Pacman's X velocity
                    self.pacman.rect.top -= self.pacman.vel[1] # go back for Pacman's Y velocity
            
            if pygame.sprite.spritecollide(self.pacman, self.pellet_sprites, True): # if pacman have eaten a pellet,
                self.pacman.score += 1 # add him some score
                self.play_sound("sound/chomp.wav") # play chomp sound
            
            self.screen.blit(self.background, (100, 0)) # blit background at position X=100, Y=0   
            self.sprites.draw(self.screen) # Draw non-pellet sprites
            self.pellet_sprites.draw(self.screen) # Draw pellets' sprites

            if pygame.font:
                font = pygame.font.SysFont("tahoma", 36) # set font family = "Tahoma", with size = 36
                text = font.render("Score: %s" % self.pacman.score, 1, (255, 0, 0)) # Create "Score" line
                textrect = text.get_rect(centerx=self.width / 2) # Text rectangle (position source)
                self.screen.blit(text, textrect) # Show "Score" line at the top of the screen
            
            pygame.display.flip() # update the screen

            if self.move: # if Pacman should move,
                self.pacman.move(self.key) # he must do it

class Pacman(pygame.sprite.Sprite):
    """ Pacman class. """
    def __init__(self, master):
        pygame.sprite.Sprite.__init__(self) # initializing the base pygame.sprite.Sprite class
        pygame.time.set_timer(31, 150) # create event for changing Pacman's sprite costume (ID=31), and then handle it
        self.costumes = itertools.cycle((pygame.image.load("images/pacman/yellow/open/medium.png"), pygame.image.load(r"images/pacman/yellow/close.png"))) # iterable, which returns opened or closed mouth alternately
        self.image = pygame.image.load(r"images/pacman/yellow/open/medium.png") # set Pacman's base image (self.image)
        self.rect = self.image.get_rect() # get rectangle of Pacman's sprite
        self.rect.left = 300 # set start position by X
        self.rect.top = 315 # set start position by Y
        self.vel = [0,0] # set Pacman's velocity
        self.score = 0 # game score variable
        self.master = master # sprite master
        self.rotated = False # check if Pacman is rotated (because every rotating stops Pacman's mouth opening/closing)
    def move(self, key):
        """ Moves the Pacman. """
        if key == K_LEFT: # if key is LEFT ARROW KEY,
            self.vel = [-5, 0] # set Pacman's velocity,
            if not self.rotated: # if is not rotated yet,
                self.costumes = itertools.cycle((pygame.transform.rotate(pygame.image.load("images/pacman/yellow/open/medium.png"), 90),
                                                 pygame.transform.rotate(pygame.image.load(r"images/pacman/yellow/close.png"), 90))) # rotate costumes,
                self.rotated = True # and it's rotated now!
        elif key == K_UP: # if key is UP ARROW KEY,
            self.vel= [0, -5] # set Pacman's velocity,
            if not self.rotated: # if is not rotated yet,
                self.costumes = itertools.cycle((pygame.image.load("images/pacman/yellow/open/medium.png"),
                                                pygame.image.load(r"images/pacman/yellow/close.png"))) # rotate costumes,
                self.rotated = True # and it's rotated now!

        elif key == K_RIGHT: # if key is RIGHT ARROW KEY,
            self.vel = [5, 0] # set Pacman's velocity,
            if not self.rotated: # if is not rotated yet,
                self.costumes = itertools.cycle((pygame.transform.rotate(pygame.image.load("images/pacman/yellow/open/medium.png"), -90),
                                                 pygame.transform.rotate(pygame.image.load(r"images/pacman/yellow/close.png"), -90))) # rotate costumes,
                self.rotated = True # and it's rotated now!
                
        elif key == K_DOWN: # if key is DOWN ARROW KEY,
            self.vel = [0, 5] # set Pacman's velocity,
            if not self.rotated: # if is not rotated yet,
                self.costumes = itertools.cycle((pygame.transform.rotate(pygame.image.load("images/pacman/yellow/open/medium.png"), 180),
                                                 pygame.transform.rotate(pygame.image.load(r"images/pacman/yellow/close.png"), 180))) # rotate costumes,
                self.rotated = True # and it's rotated now!
        pygame.time.wait(10) # wait 10ms, otherwise Pacman will run too fast

        self.rect.left += self.vel[0] # move by X
        self.rect.top += self.vel[1] # move by Y
        if self.rect.left < 102 and self.rect.top in range(255, 301): # if Pacman went out of left bounds,
            self.rect.left = 535 # set its coords by X
            self.rect.top = 270 # set its coords by Y
        elif self.rect.left > 535 and self.rect.top in range(255, 301): # if Pacman went out of right bounds,
            self.rect.left = 102 # set its coords by X
            self.rect.top = 270 # set its coords by Y
    def next_costume(self):
        """ Opens or closes Pacman's costume. """
        self.image = next(self.costumes) # set pacman image to next from opened/closed mouth
        self.spos = (self.rect.left, self.rect.top) # save old image position (because it will come always to X=0, Y=0 position)
        self.rect = self.image.get_rect() # get image rectangle
        self.rect.left = self.spos[0] # set left of rectangle to old X
        self.rect.top = self.spos[1] # set top of rectangle to old Y

class Pellet(pygame.sprite.Sprite):
    """ Pellet (dot) class. """
    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self) # initializing the base pygame.sprite.Sprite class
        self.image = pygame.image.load('images/dot/medium.png') # load pellet's sprite image
        if rect: self.rect = rect # if rect is specified, set it as self.rect
        else: self.rect = self.image.get_rect() # else, set image rect as self.rect
            
if __name__ == "__main__":
    main = Main() # create the game
    main.mainloop() # start mainloop of the game
