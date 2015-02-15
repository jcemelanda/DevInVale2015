from random import randrange
from os.path import join
import pygame
from pygame.rect import Rect
from pygame.sprite import Sprite, Group, GroupSingle

__author__ = 'julio'


class Ship(Sprite):
    def __init__(self, img_name, width, height, game):
        super().__init__()

        self.image = pygame.image.load(img_name).convert_alpha()
        self.rect = Rect(454, 516, width, height)
        self.exploded = False
        self.game = game

    def update(self):
        if not self.exploded:
            if self.game.ship_collides:
                self.exploded = True
                return

            x_move = 0
            y_move = 0
            if self.game.input.up_pressed:
                y_move -= 20
            elif self.game.input.down_pressed:
                y_move += 20
            if self.game.input.left_pressed:
                x_move -= 20
            if self.game.input.right_pressed:
                x_move += 20
            if self.game.input.space_pressed:
                self.game.elements[-3].add(LaserSprite(join('gfx', 'laser.png'), self.rect, self.game))
            self.rect = self.rect.move(x_move, y_move)
        else:
            self.groups()[-1].add(AnimatedShip(join('gfx', 'ship_exploded.png'),
                                              self.rect,
                                              3,
                                              self.game))



class AnimatedShip(Sprite):
    def __init__(self, img_name, rect, sprite_count, game):
        super().__init__()

        self.image = pygame.image.load(img_name).convert_alpha()
        self.rect = rect
        self.visible_rect = Rect(0, 0, rect.width, rect.width)
        self.explosion_step = 0
        self.game = game
        self.finished = False
        self.sprite_count = sprite_count

    def update(self):
        self.visible_rect = Rect(self.explosion_step*self.rect.width,
                                 self.explosion_step*self.rect.height,
                                 self.rect.width,
                                 self.rect.height)
        self.explosion_step += 1
        if self.explosion_step == self.sprite_count:
            self.groups()[0].add(TextSprite('GAME OVER', self.game))
            self.game.game_over = True
            self.kill()


class ShipGroup(GroupSingle):
    def draw(self, surface):
        for sprite in self.sprites():
            params = [sprite.image, sprite.rect]
            try:
                params.append(sprite.visible_rect)
            except:
                pass

            self.spritedict[sprite] = surface.blit(*params)
        self.lostsprites = []


class Asteroid(Sprite):
    def __init__(self, img_name, width, height):
        super().__init__()

        self.image = pygame.image.load(img_name).convert_alpha()
        self.rect = Rect(randrange(956-width), -100, width, height)
        self.y_speed = randrange(10, 30)


    def update(self, *args):
        x_move = 0
        y_move = self.y_speed

        self.rect = self.rect.move(x_move, y_move)


class AsteroidGroup(Group):
    def __init__(self, img_name, *sprites):
        super().__init__(*sprites)
        self.img_name = img_name
        self.new_asteroid_countdown = 10

    def update(self, *args):
        self.new_asteroid_countdown -= 1
        if not self.new_asteroid_countdown:
            self.add(Asteroid(self.img_name, 64, 64))
            self.new_asteroid_countdown = 10

        super().update(*args)


class TextSprite(Sprite):
    def __init__(self, text, game):
        self.image = game.game_font.render(text, 1, (255, 0, 0))
        self.rect = self.image.get_rect().move(335, 250)
        super().__init__()


class ScoreSprite(Sprite):
    def __init__(self, game):
        self.score_text = 'Score: {}'
        self.game = game
        self.game.score = 0
        self.image = game.score_font.render(self.score_text.format(self.game.score), 1, (255, 255, 220))
        self.rect = self.image.get_rect().move(15, 15)
        self.game = game
        self.score_countdown = 10
        super().__init__()

    def update(self, *args):
        super().update()
        if not self.game.game_over:
            if self.score_countdown:
                self.game.score += 1
                self.score_countdown -= 1
            else:
                self.score_countdown = 10
            self.image = self.game.score_font.render(self.score_text.format(self.game.score), 1, (255, 255, 220))


class LaserSprite(Sprite):
    def __init__(self, img_name, rect, game):
        self.image = pygame.image.load(img_name).convert_alpha()
        self.rect = Rect(rect.centerx, rect.centery, 2, 9)
        super().__init__()

    def update(self, *args):
        super().update()
        self.rect = self.rect.move(0, -20)
