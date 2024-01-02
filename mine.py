import time
from pygame.sprite import Sprite
from random import randint, random as rand
from pygame.transform import rotate
from pygame.mask import from_surface
from ship import Ship
from resources import *

class Mine(Sprite):
    critical_chance = 0.2

    def __init__(self, x, y):
        super().__init__()
        self.image = rotate(spritesheet["mine"][0], randint(-360, 360))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = from_surface(self.image)
        
        self.normal_damage = randint(Ship.MAX_LIFE // 16, Ship.MAX_LIFE // 15)
        self.critical_damage = randint(Ship.MAX_LIFE // 13, Ship.MAX_LIFE // 11)

        if rand() < self.critical_chance:
            self.damage = self.critical_damage
        else:
            self.damage = self.normal_damage

    def update(self):
        pass
        