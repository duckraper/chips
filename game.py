import pygame as pg
from pygame.sprite import collide_mask
from data.vfx.ParticleGroup import ParticleGroup
from data.vfx.StarParticle import StarParticle
from data.vfx.explosion import Explosion
from time import time
from resources import *
from ship import Ship
from random import randint, random as rand
from mine import Mine
from debug import debug
from math import sqrt

class Game:
    def __init__(self) -> None:
        self.running = False
        self.__paused = False
        self.fullscreen = False
        get_joystick()
        self.font = get_font()

        mines_offset = 400
        left_ship = Ship("left", (mines_offset, screen_height // 2), 90)
        right_ship = Ship("right", (screen_width - mines_offset, screen_height // 2), -90)
        
        self.ships = pg.sprite.Group(left_ship, right_ship)

        self.left_ship = pg.sprite.GroupSingle(left_ship)
        self.right_ship = pg.sprite.GroupSingle(right_ship)

        self.shots = pg.sprite.Group()
        self.mines = pg.sprite.Group()
        self.max_mines = 5
        self.mines_spawn_prob = randint(1, 2) / 1000

        self.stars = ParticleGroup(randint(5, 10), StarParticle)
        self.explosions = ParticleGroup(0, Explosion)
        self.timer = time()
        
        # control del flujo de tiempo
        self.elapsed_time = time()
        self.delta = time() - self.elapsed_time

    def spawner(self) -> None:
        if rand() < self.mines_spawn_prob:
            mine: Mine | None = self.spawn_mine()
            if mine is not None:
                self.mines.add(self.spawn_mine())


    def spawn_mine(self) -> Mine | None:
        if len(self.mines.sprites()) >= self.max_mines:
            return

        mines_offset = spritesheet["mine"][0].get_width()
        x = randint(0, screen_width) 
        y = randint(0, screen_height)

        for ship in self.ships.sprites():
            x2, y2 = ship.rect.center
            distance = sqrt((x2 - x)**2 + (y2 - y)**2)
            if distance < 150:
                return self.spawn_mine()

        for mine in self.mines.sprites():
            x2, y2 = mine.rect.center
            distance = sqrt((x2 - x)**2 + (y2 - y)**2)
            if distance < mines_offset * 2:
                return self.spawn_mine()

        mine = Mine(x, y)
        return mine

    def __shot_w_ship_collisions(self, ship, other_ship):
        collided_shots = pg.sprite.spritecollide(
            sprite=ship.sprite, group=other_ship.sprite.shots, dokill=True, collided=collide_mask)

        if collided_shots:
            ship.sprite.get_damage(sum(shot.damage for shot in collided_shots))
            ship.sprite.shake(vertical=True, horizontal=True)
            for shot in collided_shots:
                x, y = shot.rect.center
                explosion_size = (25, 25)
                explosion = Explosion(x, y, explosion_size)
                self.explosions.particles.append(explosion)

    def __handle_collisions(self) -> None:
        """
        Controla las posiciones de los sprites para asi
        controlar si existio collision entre ellos y poder hacer algo
        al respecto si sucede
        """
        self.__shot_w_ship_collisions(self.left_ship, self.right_ship)
        self.__shot_w_ship_collisions(self.right_ship, self.left_ship)

        # collision de naves con minas
        ship_w_mines_collision = pg.sprite.groupcollide(
            self.ships, self.mines, 0, 1, collided=collide_mask)

        if ship_w_mines_collision:
            for ship, mines in ship_w_mines_collision.items():
                for mine in mines:
                    ship.get_damage(mine.damage)
                    ship.shake(amplitude=10)
                    x, y = mine.rect.center
                    explosion_size = (50, 50)
                    explosion = Explosion(x, y, explosion_size)
                    self.explosions.particles.append(explosion)

        # collision de los disparos entre si
        shot_w_shot_collision = pg.sprite.groupcollide(
            self.left_ship.sprite.shots, self.right_ship.sprite.shots,
            1, 1, collided=collide_mask)

        if shot_w_shot_collision:
            for left_shot, right_shot in shot_w_shot_collision.items():
                x, y = left_shot.rect.center
                explosion_size = (10, 10)
                explosion = Explosion(x, y, size=explosion_size)
                self.explosions.particles.append(explosion)

        # collision de las naves entre si
        ship_w_ship_collision = pg.sprite.groupcollide(self.left_ship, self.right_ship, 0, 0,
                                      collided=collide_mask)
        
        if ship_w_ship_collision:
            collision_damage = 0.5
            for ship in self.ships:
                ship.get_damage(collision_damage)
                ship.set_speed(int(Ship.speed * 0.8))
                ship.shake(amplitude=10)

        else:
            for ship in self.ships:
                ship.set_speed(int(Ship.speed))

    def update(self) -> None:
        for ship in self.ships:
            if ship.shots:
                for shot in ship.shots:
                    self.shots.add(shot)

        self.delta: float = time() - self.elapsed_time
        self.elapsed_time: float = time()

    def countdown(self, counting=["3", "2", "1", "Go!"]) -> None:
        for i in counting:
            text = self.font.render(str(i), True, (255, 255, 255))
            rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

            initial_time = time()
            while time() - initial_time < 1:
                
                alpha = int(max(0, 255 - (time() - initial_time) * 300))
                text.set_alpha(alpha)

                pg.display.get_surface().fill(colors["black"])
                pg.display.get_surface().blit(text, rect)
                self.stars.draw()
                pg.display.flip()
        
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

        ######### temporal ##########
        self.left_ship.sprite.rotation += 1
        self.left_ship.sprite.shoot()
        #############################

        if not self.__paused:
            self.spawner()
            self.mines.update()
            self.stars.update(self.delta)
            self.explosions.update(self.delta)
            self.ships.update(self.delta)

            if len(self.ships.sprites()) >= 2:
                self.__handle_collisions()

        elif self.__paused:
            self.font.render("PAUSED", 1, colors["white"])

        self.stars.draw(screen)
        self.mines.draw(screen)
        self.explosions.draw(screen)
        self.ships.draw(screen)
        
        self.update()
