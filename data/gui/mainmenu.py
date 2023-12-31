import pygame as pg
from resources import screen, screen_width, screen_height, colors, font_size, script_directory, game_title
from data.vfx.ParticleGroup import ParticleGroup
from data.vfx.StarParticle import StarParticle
from time import time
from random import randint, choice

class MainMenu:
    def __init__(self):
        self.running = True

        self.title_font = pg.font.Font(script_directory.joinpath("data", "fonts", "Pixeled.ttf"), font_size + font_size//1)
        self.option_font = pg.font.Font(script_directory.joinpath(
            "data", "fonts", "Pixeled.ttf"), font_size - font_size//3)

        self.stars = ParticleGroup(randint(5, 10), StarParticle)
        self.buttons = ["PvP", "Options", "Quit"]
        self.index = 0
        self.execute = False
        self.delta: float = 0
        self.elapsed_time: float = time()

    def get_input(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.index = (self.index - 1) % len(self.buttons)
                elif event.key == pg.K_DOWN:
                    self.index = (self.index + 1) % len(self.buttons)
                if event.key == pg.K_RETURN:
                    self.execute = True
            if event.type == pg.KEYUP:
                self.execute = False

    def get(self) -> str | None:
        """devuelve la opcion seleccionada"""
        if self.execute:
            return self.buttons[self.index]
        return

    def update(self):
        self.get_input()
        self.stars.update(self.delta)
        self.delta: float = time() - self.elapsed_time
        self.elapsed_time: float = time()
        
        
    def draw_menu(self):
        screen.fill(colors["black"])
        title_text = self.title_font.render(game_title, True, colors['white'])
        title_rect = title_text.get_rect(center=(screen_width// 2, screen_height // 4))

        screen.blit(title_text, title_rect)

        for i, option in enumerate(self.buttons):
            option_color = choice([colors["blue"], colors["red"]]) if i == self.index else colors['white']
            option_text = self.option_font.render(option, True, option_color)
            option_rect = option_text.get_rect(
                center=(screen_width// 2, screen_height // 2 + i * 60))
            screen.blit(option_text, option_rect)
        self.stars.draw()