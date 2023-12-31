from data.vfx.Particle import Particle
from random import randint, uniform
from resources import generate_light_color, screen_width, screen_height, screen
from pygame import draw

class StarParticle(Particle):
    def __init__(self) -> None:
        x = randint(0, screen_width)
        y = randint(0, screen_height)
        self.color: tuple[int, int, int] = generate_light_color()
        self.radius = randint(1,2)
        self.speed = randint(1, 40)
        super().__init__(x, y, size=(0,0))

    def move(self, delta):
        self.x -= self.speed * delta
        if self.x < 0:
            self.reset_position()

    def reset_position(self):
        self.x = screen_width
        self.y = randint(0, screen_height)

    def draw(self, screen):
        draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def update(self, delta):
        self.move(delta)