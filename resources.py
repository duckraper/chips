"""ARCHIVO DE RECURSOS E IMPORTACIONES PARA EL JUEGO"""

import pygame as pg
import random
from pathlib import Path
from pygame.surface import Surface
from pygame.math import Vector2
from time import time

pg.display.init()

monitor_size = (pg.display.Info().current_w, pg.display.Info().current_h)
screen_size = (monitor_size[1] - 100, monitor_size[1] - 100)
screen_width, screen_height = screen_size

screen: Surface = pg.display.set_mode(screen_size, pg.NOFRAME)
print(screen_size)

FPS = 60

SPRITE_SIZE: tuple[int, int] = (screen_width//15, screen_width // 15)

font_size = 60

script_directory: Path = Path(__file__).resolve().parent

pg.joystick.init()

joy_count = 0
joysticks: list[pg.joystick.JoystickType] = []


def load_image(filepath) -> Surface:
    return pg.image.load(filepath).convert_alpha()


def load_sprites(directory, file_pattern, size=SPRITE_SIZE, colorkey=None) -> list[Surface]:
    sprite_list: list[Surface] = []
    files: int = len(list(script_directory.joinpath(
        "data", directory).iterdir()))

    for i in range(files):
        sprite_filepath: Path = script_directory.joinpath(
            "data", directory, file_pattern.format(i=i))
        frame = pg.transform.scale(load_image(str(sprite_filepath)), size)
        
        if colorkey is not None:
            frame.set_colorkey(colorkey)

        sprite_list.append(frame)

    return sprite_list

spritesheet: dict[str, list[Surface]] = {
    "left_ship": load_sprites("sprites/ships/left", "left_ship-0{i}.png"),
    "right_ship": load_sprites("sprites/ships/right", "right_ship-0{i}.png"),
    "left_attack": load_sprites("sprites/ships/left-attack", "left_ship_attack-0{i}.png"),
    "right_attack": load_sprites("sprites/ships/right-attack", "right_ship_attack-0{i}.png"),
    "little_blast": load_sprites("sprites/blasts/little_blast", "little_blast-0{i}.png"),
    "spear_blast": load_sprites("sprites/blasts/spear_blast", "spear_blast-0{i}.png"),
    "explosion": load_sprites("vfx/explosion", "explosion-0{i}.png"),
    "normal_shot": load_sprites("sprites/blasts/normal_shot", "normal_shot-0{i}.png"),
    "life_bar": load_sprites("gui/life_bar", "life_bar-{i}.png", size=(64*3,18*1.5), colorkey=(18, 22, 3)),
    "mine": load_sprites("sprites/extras/mine", "mine-{i}.png", size=(SPRITE_SIZE[0]//3,SPRITE_SIZE[1]//3))
}

colors = {
    "blue": (32, 41, 135),
    "black": (18, 22, 25),
    "jasmine": (244, 213, 141),
    "pink": (147, 47, 109),
    "gray": (154, 160, 168),
    "red": (135, 27, 27),
    "white": (250, 250, 250)
}

movement: dict[str, Vector2] = {
    "up": Vector2(0, -1),
    "down": Vector2(0, 1),
    "right": Vector2(1, 0),
    "left": Vector2(-1, 0),
}

game_title = "chips"
game_icon: Surface = spritesheet["normal_shot"][0]


def get_font(font="Pixeled.ttf", size = font_size) -> pg.font.Font:
    the_font = pg.font.Font(script_directory.joinpath("data", "fonts", font), size)

    return the_font


def between(value, min, max):
    return min <= value <= max


def get_joystick():
    for event in pg.event.get():
        if event.type == pg.JOYDEVICEADDED:
            joysticks.append(pg.joystick.Joystick(event.device_index))
            joy_count = pg.joystick.get_count()
            print(f"Joystick {event.device_index} connected\n"
                  f"actual joysticks: {joy_count}")


def calculate_speed(base_speed, width=screen_width):
    scale_factor = width // 600
    adaptive_speed = int(base_speed * scale_factor)
    return adaptive_speed


def generate_light_color() -> tuple[int, int, int]:
    # Generar valores de color claro
    red_channel = random.randint(180, 255)
    green_channel = random.randint(180, 255)
    blue_channel = random.randint(160, 255)

    # Agregar variabilidad al color para evitar colores oarecidos
    variation = random.randint(0, 30)
    red_channel = min(255, red_channel + variation)
    green_channel = min(255, green_channel + variation)
    blue_channel = min(255, blue_channel + variation)

    return red_channel, green_channel, blue_channel

def announcement(self, message: list[str] | str, color=colors["white"], x: int=screen_width // 2, y: int=screen_height // 2) -> None:
    for i in message:
        text = self.font.render(str(i), True, color)
        rect = text.get_rect(center=(x, y))

        initial_time = time()
        message_delay = 1
        fading = 300
        while time() - initial_time < message_delay:
            
            alpha = int(max(0, 255 - (time() - initial_time) * fading))
            text.set_alpha(alpha)

            # Dibujar en pantalla
            pg.display.get_surface().fill(colors["black"])
            pg.display.get_surface().blit(text, rect)
            self.stars.draw()
            pg.display.flip()
