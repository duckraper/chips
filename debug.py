"""
PROGRAMA CREADO CON EL FIN DE MOSTRAR EN PANTALLA
COSAS EQUIS QUE ME HAGAN FALTA MONITOREAR MIENTRAS PROGRAMO
ES TIPO UNA HERRAMIENTA GENERAL QUE ME SIRVE EN CUALQUIER PROYECTO
"""

import pygame as pg

pg.init()
font = pg.font.Font(None, 30)


def debug(info, x=10, y=10) -> None:
    display_surface = pg.display.get_surface()
    debug_surf = font.render(str(info), True, "black")
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pg.draw.rect(display_surface, "white", debug_rect, width=0)
    display_surface.blit(debug_surf, debug_rect)
