"""Module recovery_potions."""
__author__ = 'Joan A. Pinol  (japinol)'

from enum import Enum
from random import randint

import pygame as pg

from snakes.actors import Actor, ActorType
from snakes.colors import Color
from snakes import lib_jp
from snakes import resources
from snakes.settings import Settings


class RecoveryPotionType(Enum):
    """RecoveryPotion types."""
    T1_HEALTH = 'health'
    T2_POWER = 'power'


class RecoveryPotion(pg.sprite.Sprite):
    """Represents a recovery potion."""
    actor_type = ActorType.RECOVERY_POTION
    cell_added_size = lib_jp.Size(w=8, h=8)     # Added size to the defined cell size.
    size = None
    sprite_images = {}
    max_qty_on_board = 10

    def __init__(self, x, y, rec_potion_type, game):
        super().__init__()
        self.images_sprite_no = 1
        self.frame = 0
        self.rect = None
        self.rec_potion_type = rec_potion_type
        self.game = game
        self.rec_potion_type_txt = None
        self.qty = randint(15, 100)
        self.stat_type = None   # the kind of stat. it replenishes

        self.rec_potion_type_txt = self.rec_potion_type.value
        self.stat_type = self.rec_potion_type
        if self.rec_potion_type == RecoveryPotionType.T1_HEALTH:
            rec_potion_type_short = 't1'
        elif self.rec_potion_type == RecoveryPotionType.T2_POWER:
            rec_potion_type_short = 't2'

        if not RecoveryPotion.sprite_images.get(self.rec_potion_type):
            image = pg.image.load(resources.file_name_get(name='im_rec_potion_', subname=rec_potion_type_short,
                                                          num=1)).convert()
            image = pg.transform.smoothscale(image, RecoveryPotion.size)
            image.set_colorkey(Color.BLACK)
            RecoveryPotion.sprite_images[self.rec_potion_type] = image
        else:
            image = RecoveryPotion.sprite_images[self.rec_potion_type]

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Add rec_potion to the active sprite list
        self.game.active_sprites.add(self)
        self.game.rec_potions.add(self)
        self.game.normal_items.add(self)

    @classmethod
    def init(cls):
        cls.size = lib_jp.Size(w=Settings.cell_size + cls.cell_added_size.w,
                               h=Settings.cell_size + cls.cell_added_size.h)
        cls._resize_images_on_cache()

    @classmethod
    def resize_images(cls):
        if not RecoveryPotion.sprite_images:
            return
        for key, image in RecoveryPotion.sprite_images.items():
            if RecoveryPotion.size.w != image.get_size()[0] or RecoveryPotion.size.h != image.get_size()[1]:
                RecoveryPotion.sprite_images[key] = pg.transform.smoothscale(image, RecoveryPotion.size)

    @classmethod
    def create_some_random_pos(cls, n, rec_potion_type, rec_potion_list, game,
                               probability_each=100):
        Actor.create_some_random_pos(actor_cls=cls, n=n, actor_type=rec_potion_type,
                                     actor_list=rec_potion_list, game=game,
                                     probability_each=probability_each)

    @classmethod
    def _resize_images_on_cache(cls):
        if not cls.sprite_images:
            return
        for key, image in cls.sprite_images.items():
            if cls.size.w != image.get_size()[0] or cls.size.h != image.get_size()[1]:
                cls.sprite_images[key] = pg.transform.smoothscale(image, cls.size)

    @staticmethod
    def create_some(rec_potions, rec_potion_list, game):
        for rec_potion in rec_potions:
            rec_potion_list.add(RecoveryPotion(rec_potion[0], rec_potion[1], rec_potion[2], game))
