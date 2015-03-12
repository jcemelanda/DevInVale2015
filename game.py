from os.path import join

import pygame

from pygame.locals import KMOD_ALT

from pygame.locals import K_SPACE
from pygame.locals import K_UP
from pygame.locals import K_DOWN
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from pygame.locals import K_F4

from pygame.locals import QUIT
from pygame.sprite import GroupSingle, spritecollideany, groupcollide, Group
from sprites import Ship, AsteroidGroup, ShipGroup, ScoreSprite
from db import DB

__author__ = 'julio'


class UserInput:
    def __init__(self):
        self.set()

    def set(self):
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.quit_pressed = False
        self.space_pressed = False


    def reset(self):
        self.set()


class Game:
    def __init__(self):
        pygame.init()
        self.config()
        self._init_screen()
        self._init_font()
        self._init_sound()
        self.game_over = False
        self.db = DB('game.db')

    def config(self):
        self.clock = pygame.time.Clock()
        self.elements = []
        self.input = UserInput()
        self.ship_collides = []


    def _init_font(self):
        pygame.font.init()
        font_name = pygame.font.get_default_font()
        self.game_font = pygame.font.SysFont(font_name, 72)
        self.score_font = pygame.font.SysFont(font_name, 38)

    def _init_screen(self):
        self.screen = pygame.display.set_mode((956, 560), 0, 32)
        pygame.display.set_caption('DevInVale 2015')

    def _init_sound(self):
        pygame.mixer.pre_init(44100, 32, 2, 4096)
        self.explosion_sound = pygame.mixer.Sound(join('sfx', 'boom.wav'))
        self.explosion_played = False

    def player_input(self):
        self.input.reset()
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_UP]:
            self.input.up_pressed = True
        elif pressed_keys[K_DOWN]:
            self.input.down_pressed = True

        if pressed_keys[K_LEFT]:
            self.input.left_pressed = True
        elif pressed_keys[K_RIGHT]:
            self.input.right_pressed = True

        if pressed_keys[K_SPACE]:
            self.input.space_pressed = True

        pressed_mods = pygame.key.get_mods()

        if pressed_mods and KMOD_ALT:
            if pressed_keys[K_F4]:
                self.input.quit_pressed = True

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.input.quit_pressed = True

    def update(self):
        for element in self.elements:
            element.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for element in self.elements:
            element.draw(self.screen)
        pygame.display.update()

    def detect_collision(self):
        if self.elements[-1].sprite:
            self.ship_collides = spritecollideany(self.elements[-1].sprite, self.elements[-2])

        if groupcollide(self.elements[-3], self.elements[-2], True, True):
            self.score_add(50)


    def score_add(self, value):
        self.score += value



    def run(self):
        background_filename = join('gfx', 'bg_big.png')
        self.background = pygame.image.load(background_filename).convert()

        self.elements.append(GroupSingle(ScoreSprite(self)))
        self.elements.append(Group())
        self.elements.append(AsteroidGroup(join('gfx', 'asteroid.png')))
        self.elements.append(ShipGroup(sprite=Ship(join('gfx', 'ship.png'), 48, 48, self)))


        while True:
            self.player_input()
            self.events()
            if self.input.quit_pressed:
                exit(0)

            self.update()
            self.draw()
            self.detect_collision()
            time_passed = self.clock.tick(30)



if __name__ == '__main__':
    game = Game()
    game.run()
