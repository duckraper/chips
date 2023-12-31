import pygame as pg
from data.vfx.Particle import Particle
from resources import spritesheet, screen
from pygame.transform import scale


class Explosion(Particle):
    __ANIMATION_SPEED = 20
    def __init__(self, x, y, size) -> None:
        super().__init__(x, y, size)
        self.position = (x, y)
        self.spritesheet = spritesheet["explosion"] 
        self.spritesheet_size = len(self.spritesheet)
        for i, frame in enumerate(self.spritesheet):
            self.spritesheet[i] = scale(frame, self.size)
        self.actual_frame = 0
        self.animation_timer = 0
        self.is_finished = False

    def animate(self, delta):
        if not self.is_finished:
            self.animation_timer += delta
            self.actual_frame = int(
                self.animation_timer * self.__ANIMATION_SPEED) % self.spritesheet_size

            if self.actual_frame >= self.spritesheet_size - 1:
                self.is_finished = True

    def update(self, delta):
        self.animate(delta)

    def draw(self, screen):
        if not self.is_finished: 
            current_frame = self.spritesheet[self.actual_frame]
            rect = current_frame.get_rect(center=self.position)
            screen.blit(current_frame, rect.center)
