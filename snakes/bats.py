"""Module bats."""
__author__ = 'Joan A. Pinol  (japinol)'

from enum import Enum
from random import randint

import pygame as pg

from snakes.actors import Actor, ActorType
from snakes.colors import Color
from snakes import constants as consts
from snakes.experience_points import ExperiencePoints
from snakes import lib_jp
from snakes import resources
from snakes.settings import Settings


class BatType(Enum):
    """Bat types."""
    T1_BLUE = 1
    T2_LILAC = 2
    T3_RED = 3


class Bat(pg.sprite.Sprite):
    """Represents a bat."""
    actor_type = ActorType.BAT
    cell_added_size = lib_jp.Size(w=0, h=0)     # Added size to the defined cell size.
    cell_size_multiplier = 2.6
    cell_size_ratio = 1.79
    size = None
    sprite_images = {}
    max_qty_on_board = consts.MAX_BATS_ON_BOARD

    def __init__(self, x, y, bat_type, game, change_x=0, change_y=0):
        super().__init__()
        self.images_sprite_no = 4
        self.frame = randint(0, self.images_sprite_no - 1)
        self.rect = None
        self.bat_type = bat_type
        self.game = game
        self.bat_type_txt = None
        self.attack_power = None
        self.health_total = None
        self.health = None
        self.boundary_left = None
        self.boundary_right = None
        self.boundary_top = None
        self.boundary_bottom = None
        self.change_x = change_x
        self.change_y = change_y
        self.direction = consts.DIRECTION_RIGHT
        self.animate_timer = pg.time.get_ticks()
        self.drop_item_pct = 100

        walking_frames = []

        if self.bat_type == BatType.T1_BLUE:
            self.bat_type_txt = 'bats_t01'
            bat_type_short = 't1'
            self.attack_power = 10
            self.health_total = 90
            self.drop_item_pct = 100
        elif self.bat_type == BatType.T2_LILAC:
            self.bat_type_txt = 'bats_t02'
            bat_type_short = 't2'
            self.attack_power = 13
            self.health_total = 120
            self.drop_item_pct = 100
        elif self.bat_type == BatType.T3_RED:
            self.bat_type_txt = 'bats_t03'
            bat_type_short = 't3'
            self.attack_power = 18
            self.health_total = 240
            self.drop_item_pct = 100

        if not Bat.sprite_images.get(self.bat_type):
            image_quality = '_md' if Settings.cell_size >= consts.CELL_SIZE_MIN_FOR_IM_MD else ''
            for i in range(self.images_sprite_no):
                image = pg.image.load(resources.file_name_get(name='im_bat_', subname=bat_type_short,
                                                              quality=image_quality, num=i+1)).convert()
                image = pg.transform.smoothscale(image, Bat.size)
                image.set_colorkey(Color.BLACK)
                walking_frames.append(image)
            Bat.sprite_images[self.bat_type] = (image, walking_frames)
        else:
            image = Bat.sprite_images[self.bat_type][0]

        if self.change_x > 0:
            self.direction = consts.DIRECTION_RIGHT
        elif self.change_x < 0:
            self.direction = consts.DIRECTION_LEFT

        self.image = Bat.sprite_images[self.bat_type][1][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.initialize_boundaries()

        self.health = self.health_total

        # Add bat to the active sprite list
        self.game.active_sprites.add(self)
        self.game.bats.add(self)

    def initialize_boundaries(self):
        if self.change_x:
            self.boundary_left = 0
            self.boundary_right = Settings.screen_width - self.rect.w
        if self.change_y:
            self.boundary_top = Settings.screen_near_top
            self.boundary_bottom = Settings.screen_height - self.rect.h

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # Calculate frame of the animated sprite
        if self.game.current_time - self.animate_timer > Settings.fps * 5:
            self.animate_timer = self.game.current_time
            self.frame = self.frame + 1 if self.frame < self.images_sprite_no - 1 else 0
            self.image = Bat.sprite_images[self.bat_type][1][self.frame]

        # Check boundaries and see if we need to reverse direction.
        if self.change_y:
            if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
                self.change_y *= -1
                self.direction = consts.DIRECTION_UP if self.change_y < 0 else consts.DIRECTION_DOWN
        if self.change_x:
            if self.rect.x < self.boundary_left or self.rect.x > self.boundary_right:
                self.change_x *= -1
                self.direction = consts.DIRECTION_LEFT if self.change_x < 0 else consts.DIRECTION_RIGHT

        # Check if it hit any bullet
        bullet_hit_list = pg.sprite.spritecollide(self, self.game.bullets, False)
        for bullet in bullet_hit_list:
            bullet.kill()
            self.health -= bullet.attack_power
            if self.health < 1:
                self.game.sound_effects and resources.Resource.bat_scream_sound.play()
                self.kill()
                bullet.owner.stats['bats'] += 1
                bullet.owner.stats[self.bat_type_txt] += 1
                bullet.owner.stats['score'] += ExperiencePoints.xp_points[self.bat_type_txt]
            else:
                self.game.sound_effects and resources.Resource.bullet_hit_sound.play()

    def draw_health(self):
        Actor.draw_health(self)

    def drop_item(self):
        pass

    @classmethod
    def init(cls):
        if Settings.cell_size < 6:
            cls.cell_added_size = lib_jp.Size(w=round(5*Bat.cell_size_ratio), h=5)
        elif Settings.cell_size < 9:
            cls.cell_added_size = lib_jp.Size(w=round(3*Bat.cell_size_ratio), h=3)
        cls.size = lib_jp.Size(w=round(Settings.cell_size * Bat.cell_size_ratio
                               * Bat.cell_size_multiplier + cls.cell_added_size.w),
                               h=round(Settings.cell_size * Bat.cell_size_multiplier
                                       + cls.cell_added_size.h))
        cls._resize_images_on_cache()

    @classmethod
    def create_some_random_pos(cls, n, bat_type, bat_list, game, probability_each=100):
        Actor.create_some_random_pos(actor_cls=cls, n=n, actor_type=bat_type,
                                     actor_list=bat_list, game=game,
                                     probability_each=probability_each)

    @classmethod
    def _resize_images_on_cache(cls):
        if not cls.sprite_images:
            return
        for key, tuple_images in cls.sprite_images.items():
            if (cls.size.w != tuple_images[0].get_size()[0]
                    or cls.size.h != tuple_images[0].get_size()[1]):
                cls.sprite_images[key] = pg.transform.smoothscale(tuple_images[0], cls.size)
