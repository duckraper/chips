from blast import Blast, spritesheet,SPRITE_SIZE, colors, screen_width, screen_height
from pygame.mask import from_surface
from pygame.surface import Surface
from pygame.transform import rotate, scale

class NormalShot(Blast):
    def __init__(self, side, x, y, speed, rotation, damage=10, size=(6,15)):
        super().__init__(side, x, y, speed, rotation, damage, size)

        if side == "left":
            self.image = spritesheet["normal_shot"][0]
        if side == "right":
            self.image = spritesheet["normal_shot"][1]

        self.image = rotate(scale(self.image, size), rotation)
        self.rect = self.image.get_rect(center = (x, y))
        self.mask = from_surface(self.image)

    def update(self, delta) -> None:
        return super().update(delta)