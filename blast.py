from pygame.sprite import Sprite
from pygame.surface import SurfaceType, Surface
from pygame.transform import rotate, scale
from pygame.mask import from_surface
from math import cos, sin, radians

from resources import *


class Blast(Sprite):
    def __init__(self, side, x, y, speed, rotation, damage, size) -> None:
        super().__init__()

        self.side: str = side
        self.speed: int = speed
        self.damage: int = damage
        self.rotation = rotation
        self.radians = radians(self.rotation)
        self.size = size
        self.image = rotate(Surface(size), self.rotation)
        self.mask = from_surface(self.image)
        self.rect = self.image.get_rect(center=(x, y))


    def __constraints(self) -> None:
        if not 0 < self.rect.centerx <= screen_width or not 0 < self.rect.centery <= screen_height:
            self.kill()

    def __move(self, delta):
        dx = self.speed * sin(self.radians)
        dy = self.speed * cos(self.radians)

        self.rect.x -= dx * delta
        self.rect.y -= dy * delta

    def update(self, delta) -> None:
        self.__move(delta)
        self.__constraints()
