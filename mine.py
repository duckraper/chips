import time
from pygame.sprite import Sprite
from random import randint, random as rand
from pygame.transform import rotate
from pygame.mask import from_surface
from ship import Ship
from resources import *

class Mine(Sprite):
    normal_damage = randint(Ship.MAX_LIFE // 12, Ship.MAX_LIFE // 10)
    critical_damage = randint(Ship.MAX_LIFE // 7, Ship.MAX_LIFE // 6)
    critical_chance = 0.08
    detone_time = 200

    def __init__(self, x, y):
        super().__init__()
        self.image = rotate(spritesheet["mine"][0], randint(-360, 360))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = from_surface(self.image)
        
        if rand() < self.critical_chance:
            self.damage = self.critical_damage
        else:
            self.damage = self.normal_damage

        self.activate = False
        self.elapsed_time = 0

    def update(self):
        if self.activate:
            current_time = time.time()
            self.elapsed_time = time.time()
            if current_time - self.elapsed_time >= self.detone_time:
                print("exploto")
        