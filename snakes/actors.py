"""Module actors."""
__author__ = 'Joan A. Pinol  (japinol)'

from enum import Enum
from random import randint

import pygame as pg

from snakes import lib_jp
from snakes import lib_graphics_jp as libg_jp
from snakes.settings import Settings


class ActorType(Enum):
    """Actor types."""
    APPLE = 1
    MINE = 2
    BAT = 3
    BULLET = 4
    CARTRIDGE = 5
    RECOVERY_POTION = 6


class Actor(pg.sprite.Sprite):
    """General actors operations."""
    # Security size so the sprite will not be too close to the border of the screen.
    CELL_SCREEN_SECURITY_SIZE = 1

    @staticmethod
    def initialize_actors(actor_cls_list):
        for actor_cls in actor_cls_list:
            actor_cls.init()

    @staticmethod
    def draw_health(actor):
        if actor.health < actor.health_total - 1:
            libg_jp.draw_bar_graphic(actor.game.screen,
                                     amount_pct=actor.health / actor.health_total,
                                     x=actor.rect.x + (actor.rect.width // 2)
                                     - Settings.sprite_health_bar_pos_rel.x,
                                     y=actor.rect.y - Settings.sprite_health_bar_pos_rel.y,
                                     bar_width=Settings.sprite_health_bar_size.w,
                                     bar_height=Settings.sprite_health_bar_size.h,
                                     bar_without_outline=True)

    @staticmethod
    def create_some_random_pos(actor_cls, n, actor_type, actor_list, game,
                               probability_each=100):
        """Creates some actors of the specified type in random positions of the board."""
        ITERATIONS_MAX = 12
        cell_size = lib_jp.Size(w=actor_cls.size.w, h=actor_cls.size.h)
        cell_size_with_border = lib_jp.Size(w=cell_size.w + Actor.CELL_SCREEN_SECURITY_SIZE,
                                            h=cell_size.h + Actor.CELL_SCREEN_SECURITY_SIZE)
        cell_total_security_border = lib_jp.Size(w=actor_cls.cell_added_size.w
                                                 + Actor.CELL_SCREEN_SECURITY_SIZE,
                                                 h=actor_cls.cell_added_size.h
                                                 + Actor.CELL_SCREEN_SECURITY_SIZE)
        if len(actor_list) >= actor_cls.max_qty_on_board:
            return
        elif n + len(actor_list) >= actor_cls.max_qty_on_board:
            n = actor_cls.max_qty_on_board - len(actor_list)
        iterations = 0
        for _ in range(n):
            if probability_each < 100 and randint(1, 100) > probability_each:
                continue
            actor_added = False
            iterations = 0
            actor_obj = None
            while not actor_added and (iterations <= ITERATIONS_MAX):
                iterations += 1
                x = randint(cell_total_security_border.w,
                            Settings.screen_width - cell_size_with_border.w)
                y = randint(Settings.screen_near_top + cell_total_security_border.h,
                            Settings.screen_height - cell_size_with_border.h)
                # Check if there is some sprite in this position
                position_not_taken = True
                rect1 = pg.Rect(x, y, cell_size.w, cell_size.h)
                if actor_cls.actor_type != ActorType.BAT:
                    # Apples and mines cannot collide with any kind of sprite
                    for sprite in game.active_sprites:
                        if rect1.colliderect(sprite.rect):
                            position_not_taken = False
                            break
                else:
                    # Bats cannot collide with snakes and other bats
                    for sprite in game.snakes:
                        if rect1.colliderect(sprite.rect):
                            position_not_taken = False
                            break
                    if position_not_taken:
                        for sprite in game.bats:
                            if rect1.colliderect(sprite.rect):
                                position_not_taken = False
                                break
                if position_not_taken:
                    actor_obj = actor_cls(x, y, actor_type, game=game)
                    if actor_obj.actor_type == ActorType.BAT:
                        actor_obj.change_x = randint(3, 5)
                        actor_obj.change_y = randint(3, 5)
                        actor_obj.initialize_boundaries()
                    actor_added = True
