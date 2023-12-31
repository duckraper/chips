import pygame as pg
from data.vfx.ParticleGroup import ParticleGroup
from data.vfx.StarParticle import StarParticle
from data.vfx.explosion import Explosion
from time import time
from resources import *
from ship import Ship
from random import randint

class Game:
    def __init__(self) -> None:
        self.running = False
        self.__paused = False
        self.fullscreen = False
        get_joystick()
        self.font = get_font()

        offset = 400
        left_ship = Ship("left", (offset, screen_height // 2), 90)
        right_ship = Ship("right", (screen_width - offset, screen_height // 2), -90)
        
        self.ships = pg.sprite.Group(left_ship, right_ship)

        self.left_ship = pg.sprite.GroupSingle(left_ship)
        self.right_ship = pg.sprite.GroupSingle(right_ship)

        self.bullets = pg.sprite.Group()

        self.stars = ParticleGroup(randint(5, 10), StarParticle)
        self.explosions = ParticleGroup(0, Explosion)

        # control del flujo de tiempo
        self.elapsed_time = time()
        self.delta = time() - self.elapsed_time

    def __handle_collisions(self) -> None:
        """
        Controla las posiciones de los sprites para asi
        controlar si existio collision entre ellos y poder hacer algo
        al respecto si sucede
        """
        left_collided_shots = pg.sprite.spritecollide(sprite=self.left_ship.sprite,
                                                          group=self.right_ship.sprite.shots,
                                                          dokill=False, collided=pg.sprite.collide_mask)
        if left_collided_shots:
            self.left_ship.sprite.get_damage(sum(shot.damage for shot in left_collided_shots))
            self.left_ship.sprite.shake(vertical=True, horizontal=True)
            for shot in left_collided_shots:
                shot.kill()

        right_collided_shots = pg.sprite.spritecollide(sprite=self.right_ship.sprite,
                                                           group=self.left_ship.sprite.shots,
                                                           dokill=True, collided=pg.sprite.collide_mask)
        if right_collided_shots:
            self.right_ship.sprite.get_damage(sum(shot.damage for shot in right_collided_shots))
            self.right_ship.sprite.shake(vertical=True, horizontal=True)
            for shot in right_collided_shots:
                shot.kill()

        # collision de los disparos entre si
        shot_collisions = pg.sprite.groupcollide(
            self.left_ship.sprite.shots, self.right_ship.sprite.shots,
            dokilla=True, dokillb=True, collided=pg.sprite.collide_mask)

        for left_shot, right_shot in shot_collisions.items():
        # Obtener la posición de la colisión y crear una explosión
            x, y = left_shot.rect.center
            explosion_size = (10, 10)
            explosion = Explosion(x, y, size=explosion_size)
            self.explosions.particles.append(explosion)

        # collision de las naves entre si
        if pg.sprite.groupcollide(self.left_ship, self.right_ship, False, False,
                                      collided=pg.sprite.collide_mask):
            """
            las naves al chocar vibraran, quitandose vida, ambas y reduciendo su velocidad
            de movimiento, haciendo asi, que ambas tengan que evitar collisionarse
            """
            collision_damage = 0.5
            for ship in self.ships:
                ship.get_damage(collision_damage)
                ship.set_speed(int(Ship.speed * 0.2))
                ship.shake(amplitude=10)

        else:
            for ship in self.ships:
                ship.set_speed(int(Ship.speed))

    def __update(self) -> None:
        self.delta: float = time() - self.elapsed_time
        self.elapsed_time: float = time()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                break

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                    break

                if event.key == pg.K_p:
                    self.toggle_pause()

            if event.type == pg.JOYBUTTONDOWN:
                if event.button == 7:
                    self.toggle_pause()

            if event.type == pg.JOYDEVICEADDED:
                joysticks.append(
                    pg.joystick.Joystick(event.device_index))
                joy_count = pg.joystick.get_count()
                print(f"joystick {event.device_index} connected\n"
                        f"\tactual joysticks: {joy_count}")

            if event.type == pg.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                joy_count = pg.joystick.get_count()
                print(f"joystick {event.instance_id} disconnected\n"
                        f"\tactual joysticks: {joy_count}")

    def toggle_pause(self) -> None:
        """Invierte el estado de pausado del juego"""
        self.__paused = not self.__paused

    def run(self) -> None:
        self.handle_events()
        screen.fill(colors['black'])

        self.left_ship.sprite.rotation += 1
        self.left_ship.sprite.shoot()

        if not self.__paused:
            self.stars.update(self.delta)
            self.explosions.update(self.delta)
            self.ships.update(self.delta)

            if len(self.ships.sprites()) >= 2:
                self.__handle_collisions()

        elif self.__paused:
            self.font.render("PAUSED", 1, colors["white"])

        self.stars.draw(screen)
        self.ships.draw(screen)
        self.explosions.draw(screen)
        self.__update()
