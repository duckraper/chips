from resources import screen_size
import random as r
from pygame import draw

class Particle:
    def __init__(self, x: int, y: int, size: tuple[int, int]) -> None:
        self.x: int = x
        self.y: int = y
        self.position = (x, y)
        self.size = size

    def update(self, delta):
        pass

    def draw(self, screen):
        pass
    