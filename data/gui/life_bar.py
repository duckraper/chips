from resources import spritesheet, screen
from pygame.transform import flip
import debug


class LifeBar:
    def __init__(self, x, y, side, total_life):
        self.side = side
        if self.side == "left":
            self.spritesheet = [
                flip(spritesheet["life_bar"][i], True, False) for i in range(len(spritesheet["life_bar"]))]
        else:
            self.spritesheet = spritesheet["life_bar"]
        self.life_bars = len(self.spritesheet)
        self.bar_index = 0
        self.image = self.spritesheet[self.bar_index]
        self.total_life = total_life
        self.position = (x, y)

    def change_bar(self, life):
        self.bar_index = self.life_bars - 1 - \
            min(max(0, int(life / self.total_life * self.life_bars)),
                self.life_bars - 1)

    def draw(self):
        screen.blit(self.spritesheet[self.bar_index], self.position)
