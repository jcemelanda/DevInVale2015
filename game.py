from os.path import join

import pygame
from pygame.constants import KMOD_CTRL, K_r

from pygame.locals import KMOD_ALT

from pygame.locals import K_SPACE
from pygame.locals import K_UP
from pygame.locals import K_DOWN
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from pygame.locals import K_F4

from pygame.locals import QUIT
from pygame.sprite import GroupSingle, spritecollideany, groupcollide, Group
from sprites import Ship, AsteroidGroup, ShipGroup, ScoreSprite, ExplodingAsteroidsGroup
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
        self.elements = {}
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
        self.explosion_sound = pygame.mixer.Sound(join('sfx', 'boom.ogg'))
        self.laser_sound = pygame.mixer.Sound(join('sfx', 'laser.ogg'))
        self.background_sound = pygame.mixer.Sound(join('sfx', 'background.ogg'))

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

        if pressed_mods and KMOD_CTRL:
            if pressed_keys[K_r]:
                if self.game_over:
                    self.restart()

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.input.quit_pressed = True

    def update(self):
        for element in self.elements.values():
            element.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for element in self.elements.values():
            element.draw(self.screen)
        pygame.display.update()

    def detect_collision(self):
        if self.elements['ship'].sprite:
            self.ship_collides = spritecollideany(self.elements['ship'].sprite, self.elements['asteroids'])

        if groupcollide(self.elements['lasers'], self.elements['asteroids'], True, True):
            self.score_add(50)

    def score_add(self, value):
        self.score += value

    def run(self):
        self.background_sound.set_volume(0.3)
        self.background_sound.play(loops=-1)
        background_filename = join('gfx', 'bg_big.png')
        self.background = pygame.image.load(background_filename).convert()

        self.elements['score'] = GroupSingle(ScoreSprite(self))
        self.elements['exploding_asteroids'] = ExplodingAsteroidsGroup()
        self.elements['lasers'] = Group()
        self.elements['asteroids'] = AsteroidGroup(join('gfx', 'asteroid.png'), self)
        self.elements['ship'] = ShipGroup(sprite=Ship(join('gfx', 'ship.png'), 48, 48, self))



        while True:
            self.player_input()
            self.events()
            if self.input.quit_pressed:
                exit(0)

            self.update()
            self.draw()
            self.detect_collision()
            time_passed = self.clock.tick(30)

    def restart(self):
        self.background_sound.stop()
        self.__init__()
        self.run()


if __name__ == '__main__':
    game = Game()
    game.run()
