import pygame.transform

from kelvin452.systems.rendering import make_sprite
from kelvin452.systems.world import Entity
from kelvin452.game import game
from kelvin452.assets import all_assets
import random


class FireEntity(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.__x = x
        self.__y = y
        huge_fire_sprite = pygame.transform.scale(all_assets.fire_sprite, (220, 180))
        self.__sprite = make_sprite(huge_fire_sprite, (x, y))

    def _spawned(self):
        self.show_sprite(self.__sprite)

    def _tick(self):
        self.__x += 500 * game.delta_time
        self.__y += 50 * game.delta_time
        if self.__x > game.viewport[0]:
            self.__x = 0
        if self.__y > game.viewport[1]:
            self.__y = 0
        self.__sprite.rect.topleft = self.__x, self.__y # type: ignore
        self.__sprite.dirty = 1

class piece1Entity(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.__x = x
        self.__y = y
        p1ed = pygame.transform.scale(all_assets.p1ed_sprite, (220, 180))
        self.__sprite = make_sprite(p1ed, (x, y))

    def _spawned(self):
        self.show_sprite(self.__sprite)

    def _tick(self):
        self.__x += 500 * game.delta_time
        self.__y += 50 * game.delta_time
        if self.__x > game.viewport[0]:
            self.__x = 0
        if self.__y > game.viewport[1]:
            self.__y = 0
        self.__sprite.rect.topleft = self.__x, self.__y # type: ignore
        self.__sprite.dirty = 1

class piece10Entity(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.__x = x
        self.__y = y
        p10ed = pygame.transform.scale(all_assets.p10ed_sprite, (220, 180))
        self.__sprite = make_sprite(p10ed, (x, y))

    def _spawned(self):
        self.show_sprite(self.__sprite)

    def _tick(self):
        self.__x += 500 * game.delta_time
        self.__y += 50 * game.delta_time
        if self.__x > game.viewport[0]:
            self.__x = 0
        if self.__y > game.viewport[1]:
            self.__y = 0
        self.__sprite.rect.topleft = self.__x, self.__y # type: ignore
        self.__sprite.dirty = 1

"""def game_start():
    for i in range(100):
        fire_entity = FireEntity(random.randint(0, 1280), random.randint(0, 720))
        game.world.spawn_entity(fire_entity)"""

def game_start():
    for i in range(50):
        p1ed_entity = piece1Entity(random.randint(0, 1280), random.randint(0, 720))
        game.world.spawn_entity(p1ed_entity)
    for i in range(50):
        p10ed_entity = piece10Entity(random.randint(0, 1280), random.randint(0, 720))
        game.world.spawn_entity(p10ed_entity)


def launch_game():
    game.initialize_game()
    game.on_start(game_start)
    game.start()

if __name__ == "__main__":
    launch_game()
