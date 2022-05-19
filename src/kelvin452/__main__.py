import pygame.transform
from pygame import Rect

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

class Piece1Entity(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.__x = x
        self.__y = y
        a = random.randint(32,64)
        p1ed = pygame.transform.scale(all_assets.p1ed_sprite, (a,a))
        self.__sprite = make_sprite(p1ed, (x, y))
        self.p1ed_rect = self.__sprite.rect

    def _spawned(self):
        self.show_sprite(self.__sprite)

    def _tick(self):
        self.__x += 200 * game.delta_time
        if self.__x > game.viewport[0]-450:
            self.__x = game.viewport[0]-450
        self.__sprite.rect.topleft = self.__x, self.__y # type: ignore
        self.__sprite.dirty = 1
        if self.p1ed_rect.colliderect(Rect(750,0,100,700)):
            game.world.destroy_entity(self)

class Entity_spawn(Entity):
    def __init__(self):
        super().__init__()
        self.compteurino = 10

    def _tick(self):
        self.compteur()

    def compteur(self):
        b = [50,100,150,200,250]
        self.compteurino -= game.delta_time
        if self.compteurino <= 0:
            for i in range(10):
                z = 0
                if z >= 5:
                    z = 0
                p1ed_entity = Piece1Entity(0, b[z])
                game.world.spawn_entity(p1ed_entity)
                z += 1
            self.compteurino = 10

class Piece10Entity(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.__x = x
        self.__y = y
        a = random.randint(32, 64)
        p10ed = pygame.transform.scale(all_assets.p10ed_sprite, (a,a))
        self.__sprite = make_sprite(p10ed, (x, y))

    def _spawned(self):
        self.show_sprite(self.__sprite)

    def _tick(self):
        self.__x += 500 * game.delta_time
        if self.__x > game.viewport[0]:
            self.__x = 0
        self.__sprite.rect.topleft = self.__x, self.__y # type: ignore
        self.__sprite.dirty = 1

def game_start():
    spawner = Entity_spawn()
    game.world.spawn_entity(spawner)
    for i in range(10):
        p1ed_entity = Piece1Entity(0, 50)
        game.world.spawn_entity(p1ed_entity)

def launch_game():
    game.initialize_game()
    game.on_start(game_start)
    game.start()

if __name__ == "__main__":
    launch_game()