"""Module bullets."""
__author__ = 'Joan A. Pinol  (japinol)'

import math
from enum import Enum
from random import randint

import pygame as pg

from snakes.actors import ActorType
from snakes.colors import Color
from snakes import constants as consts
from snakes.experience_points import ExperiencePoints
from snakes import lib_jp
from snakes import resources
from snakes.settings import Settings


BULLET_POWER_BASE = 2.4
BULLET_STD_RANGE = 350


class BulletType(Enum):
    """Bullet types."""
    T1_LASER1 = 'bullets_t01'
    T2_LASER2 = 'bullets_t02'
    T3_PHOTONIC = 'bullets_t03'
    T4_NEUTRONIC = 'bullets_t04'


class Bullet(pg.sprite.Sprite):
    """Represents a bullet."""
    actor_type = ActorType.BULLET
    cell_added_size = lib_jp.Size(w=-1, h=-1)     # Added size to the defined cell size.
    cell_size_multiplier = 1
    cell_size_ratio = 1
    size = None
    sprite_images = {}
    power_min_to_use = {BulletType.T1_LASER1: 1,
                        BulletType.T2_LASER2: 10,
                        BulletType.T3_PHOTONIC: 20,
                        BulletType.T4_NEUTRONIC: 35,
                        }
    power_consumption = {BulletType.T1_LASER1: 0.2,
                         BulletType.T2_LASER2: 0.5,
                         BulletType.T3_PHOTONIC: 3,
                         BulletType.T4_NEUTRONIC: 7,
                         }

    def __init__(self, x, y, bullet_type, game, owner, change_x=0, change_y=0):
        super().__init__()
        self.images_sprite_no = 1
        self.frame = randint(0, self.images_sprite_no - 1)
        self.rect = None
        self.bullet_type = bullet_type
        self.game = game
        self.owner = owner
        self.bullet_type_txt = None
        self.health_total = 100
        self.health = self.health_total
        self.attack_power = None
        self.bullet_range = BULLET_STD_RANGE
        self.boundary_left = None
        self.boundary_right = None
        self.boundary_top = None
        self.boundary_bottom = None
        self.change_x = change_x
        self.change_y = change_y
        self.direction = None
        self.animate_timer = self.game.current_time

        self.bullet_type_txt = self.bullet_type.value
        if self.bullet_type == BulletType.T1_LASER1:
            bullet_type_short = 't1'
            self.attack_power = BULLET_POWER_BASE
            self.bullet_range = int(self.bullet_range * 1.25)
        elif self.bullet_type == BulletType.T2_LASER2:
            bullet_type_short = 't2'
            self.attack_power = BULLET_POWER_BASE * 1.4
            self.bullet_range = int(self.bullet_range * 1.15)
        elif self.bullet_type == BulletType.T3_PHOTONIC:
            bullet_type_short = 't3'
            self.attack_power = BULLET_POWER_BASE * 3.4
        elif self.bullet_type == BulletType.T4_NEUTRONIC:
            bullet_type_short = 't4'
            self.attack_power = BULLET_POWER_BASE * 4.5

        if not Bullet.sprite_images.get((self.bullet_type, consts.DIRECTION_RIGHT)):
            image_quality = '_md' if Settings.cell_size >= consts.CELL_SIZE_MIN_FOR_IM_MD else ''

            image = pg.image.load(resources.file_name_get(name='im_bullet_', subname=bullet_type_short,
                                                          quality=image_quality, num=1)).convert()
            image = pg.transform.smoothscale(image, Bullet.size)
            image.set_colorkey(Color.BLACK)
            Bullet.sprite_images[(self.bullet_type, consts.DIRECTION_RIGHT)] = image

            image = pg.image.load(resources.file_name_get(name='im_bullet_', subname=bullet_type_short,
                                                          quality=image_quality, num=1)).convert()
            image = pg.transform.flip(image, True, False)
            image = pg.transform.smoothscale(image, Bullet.size)
            image.set_colorkey(Color.BLACK)
            Bullet.sprite_images[(self.bullet_type, consts.DIRECTION_LEFT)] = image

            image = pg.image.load(resources.file_name_get(name='im_bullet_', subname=bullet_type_short,
                                                          quality=image_quality, num=1)).convert()
            image = pg.transform.rotate(image, 90)
            image = pg.transform.smoothscale(image, Bullet.size)
            image.set_colorkey(Color.BLACK)
            Bullet.sprite_images[(self.bullet_type, consts.DIRECTION_UP)] = image

            image = pg.image.load(resources.file_name_get(name='im_bullet_', subname=bullet_type_short,
                                                          quality=image_quality, num=1)).convert()
            image = pg.transform.rotate(image, 270)
            image = pg.transform.smoothscale(image, Bullet.size)
            image.set_colorkey(Color.BLACK)
            Bullet.sprite_images[(self.bullet_type, consts.DIRECTION_DOWN)] = image

        if self.change_x > 0:
            self.direction = consts.DIRECTION_RIGHT
        elif self.change_x < 0:
            self.direction = consts.DIRECTION_LEFT
        elif self.change_y > 0:
            self.direction = consts.DIRECTION_DOWN
        elif self.change_y < 0:
            self.direction = consts.DIRECTION_UP

        self.image = Bullet.sprite_images[(self.bullet_type, consts.DIRECTION_RIGHT)]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.initialize_boundaries()

        # Add bullet to the active sprite list
        self.game.active_sprites.add(self)
        self.game.bullets.add(self)

    def initialize_boundaries(self):
        if self.change_x:
            self.boundary_left = 0
            self.boundary_right = Settings.screen_width - self.rect.w
        if self.change_y:
            self.boundary_top = 0
            self.boundary_bottom = Settings.screen_height - self.rect.h

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        self.image = Bullet.sprite_images[(self.bullet_type, self.direction)]

        # Check boundaries and see if we need to kill the bullet
        if self.boundary_left is not None:
            if (self.change_x < 0 and self.rect.x < self.boundary_left) \
                    or (self.change_x >= 0 and self.rect.x > self.boundary_right):
                self.kill()
        if self.boundary_top is not None:
            if (self.change_y < 0 and self.rect.y < self.boundary_top) \
                    or (self.change_y >= 0 and self.rect.y > self.boundary_bottom):
                self.kill()

        # Check if it hit any normal item (apples, cartridges, recovery potions...)
        item_hit_list = pg.sprite.spritecollide(self, self.game.normal_items, False)
        for item in item_hit_list:
            self.game.sound_effects and resources.Resource.bullet_hit_sound.play()
            self.kill()
            item.kill()

        # Check if it hit any mine
        mine_hit_list = pg.sprite.spritecollide(self, self.game.mines, False)
        for mine in mine_hit_list:
            self.game.sound_effects and resources.Resource.bullet_hit_sound.play()
            self.kill()
            mine.health -= self.attack_power
            if mine.health < 1:
                self.owner.stats[mine.mine_type_txt] += 1
                self.owner.stats['mines'] += 1
                self.owner.stats['score'] += ExperiencePoints.xp_points[mine.mine_type_txt]
                mine.kill()

        # Check if it hit any other bullet
        bullet_hit_list = pg.sprite.spritecollide(self, self.game.bullets, False)
        for bullet in bullet_hit_list:
            if bullet is not self:
                self.game.sound_effects and resources.Resource.bullet_hit_sound.play()
                self.kill()
                bullet.kill()

    @classmethod
    def init(cls):
        cls.size = lib_jp.Size(w=int(Settings.cell_size * Bullet.cell_size_ratio
                                     * Bullet.cell_size_multiplier + cls.cell_added_size.w),
                               h=int(Settings.cell_size * Bullet.cell_size_multiplier
                                     + cls.cell_added_size.h))
        cls._resize_images_on_cache()

    @classmethod
    def shot(cls, bullet_type, change_x, change_y, owner, game):
        if bullet_type == BulletType.T1_LASER1:
            game.sound_effects and resources.Resource.bullet_t1_sound.play()
        elif bullet_type == BulletType.T2_LASER2:
            game.sound_effects and resources.Resource.bullet_t2_sound.play()
        elif bullet_type == BulletType.T3_PHOTONIC:
            game.sound_effects and resources.Resource.bullet_t3_sound.play()
        elif bullet_type == BulletType.T4_NEUTRONIC:
            game.sound_effects and resources.Resource.bullet_t4_sound.play()

        Bullet(x=owner.rect.x + (change_x and ((owner.rect.w + 1)
                                               * int(change_x/math.fabs(change_x))) or 0),
               y=owner.rect.y + (not change_x and ((owner.rect.h + 1)
                                                   * int(change_y/math.fabs(change_y))) or 0),
               bullet_type=bullet_type, game=game, change_x=change_x,
               change_y=not change_x and change_y or 0, owner=owner)

    @classmethod
    def _resize_images_on_cache(cls):
        if not cls.sprite_images:
            return
        for key, image in cls.sprite_images.items():
            if cls.size.w != image.get_size()[0] or cls.size.h != image.get_size()[1]:
                cls.sprite_images[key] = pg.transform.smoothscale(image, cls.size)
