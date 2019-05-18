"""Module cartridges."""
__author__ = 'Joan A. Pinol  (japinol)'

from enum import Enum
from random import randint

import pygame as pg

from snakes.actors import Actor, ActorType
from snakes.bullets import BulletType
from snakes.colors import Color
from snakes import lib_jp
from snakes import resources
from snakes.settings import Settings


class CartridgeType(Enum):
    """Cartridge types."""
    T1_LASER1 = 'cartridges_t01'
    T2_LASER2 = 'cartridges_t02'
    T3_PHOTONIC = 'cartridges_t03'
    T4_NEUTRONIC = 'cartridges_t04'


class Cartridge(pg.sprite.Sprite):
    """Represents a cartridge."""
    actor_type = ActorType.CARTRIDGE
    cell_added_size = lib_jp.Size(w=6, h=6)     # Added size to the defined cell size.
    size = None
    sprite_images = {}
    max_qty_on_board = 10

    def __init__(self, x, y, cartridge_type, game):
        super().__init__()
        self.images_sprite_no = 1
        self.frame = 0
        self.rect = None
        self.cartridge_type = cartridge_type
        self.game = game
        self.cartridge_type_txt = None
        self.bullet_type = None   # the kind of bullet it replenishes

        self.cartridge_type_txt = self.cartridge_type.value
        if self.cartridge_type == CartridgeType.T1_LASER1:
            cartridge_type_short = 't1'
            self.bullet_type = BulletType.T1_LASER1
            self.qty = randint(5, 15)
        elif self.cartridge_type == CartridgeType.T2_LASER2:
            cartridge_type_short = 't2'
            self.bullet_type = BulletType.T2_LASER2
            self.qty = randint(4, 15)
        elif self.cartridge_type == CartridgeType.T3_PHOTONIC:
            cartridge_type_short = 't3'
            self.bullet_type = BulletType.T3_PHOTONIC
            self.qty = randint(2, 5)
        elif self.cartridge_type == CartridgeType.T4_NEUTRONIC:
            cartridge_type_short = 't4'
            self.bullet_type = BulletType.T4_NEUTRONIC
            self.qty = randint(2, 5)

        if not Cartridge.sprite_images.get(self.cartridge_type):
            image = pg.image.load(resources.file_name_get(name='im_cartridge_', subname=cartridge_type_short,
                                                          num=1)).convert()
            image = pg.transform.smoothscale(image, Cartridge.size)
            image.set_colorkey(Color.BLACK)
            Cartridge.sprite_images[self.cartridge_type] = image
        else:
            image = Cartridge.sprite_images[self.cartridge_type]

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Add cartridge to the active sprite list
        self.game.active_sprites.add(self)
        self.game.cartridges.add(self)
        self.game.normal_items.add(self)

    @classmethod
    def init(cls):
        cls.size = lib_jp.Size(w=Settings.cell_size + cls.cell_added_size.w,
                               h=Settings.cell_size + cls.cell_added_size.h)
        cls._resize_images_on_cache()

    @classmethod
    def resize_images(cls):
        if not Cartridge.sprite_images:
            return
        for key, image in Cartridge.sprite_images.items():
            if (Cartridge.size.w != image.get_size()[0]
                    or Cartridge.size.h != image.get_size()[1]):
                Cartridge.sprite_images[key] = pg.transform.smoothscale(image, Cartridge.size)

    @classmethod
    def create_some_random_pos(cls, n, cartridge_type, cartridge_list, game,
                               probability_each=100):
        Actor.create_some_random_pos(actor_cls=cls, n=n, actor_type=cartridge_type,
                                     actor_list=cartridge_list, game=game,
                                     probability_each=probability_each)

    @classmethod
    def _resize_images_on_cache(cls):
        if not cls.sprite_images:
            return
        for key, image in cls.sprite_images.items():
            if cls.size.w != image.get_size()[0] or cls.size.h != image.get_size()[1]:
                cls.sprite_images[key] = pg.transform.smoothscale(image, cls.size)

    @staticmethod
    def create_some(cartridges, cartridge_list, game):
        for cartridge in cartridges:
            cartridge_list.add(Cartridge(cartridge[0], cartridge[1], cartridge[2], game))
