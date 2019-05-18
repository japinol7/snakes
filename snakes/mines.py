"""Module mines."""
__author__ = 'Joan A. Pinol  (japinol)'

from enum import Enum

import pygame as pg

from snakes.actors import Actor, ActorType
from snakes.colors import Color
from snakes import constants as consts
from snakes import lib_jp
from snakes import resources
from snakes.settings import Settings


MINE_T01_ATTACK_POWER = 22
MINE_T02_ATTACK_POWER = 50


class MineType(Enum):
    """Mine types."""
    T1_AQUA = 1
    T2_LILAC = 2


class Mine(pg.sprite.Sprite):
    """Represents a mine."""
    actor_type = ActorType.MINE
    cell_added_size = lib_jp.Size(w=5, h=5)   # Added size to the defined cell size.
    size = None
    sprite_images = {}
    max_qty_on_board = None

    def __init__(self, x, y, mine_type, game):
        super().__init__()
        self.images_sprite_no = 1
        self.frame = 0
        self.rect = None
        self.mine_type = mine_type
        self.game = game
        self.mine_type_txt = None
        self.attack_power = None
        self.health_total = None
        self.health = None

        if self.mine_type == MineType.T1_AQUA:
            self.mine_type_txt = 'mines_t01'
            mine_type_short = 't1'
            self.health_total = 12
            self.attack_power = MINE_T01_ATTACK_POWER
        elif self.mine_type == MineType.T2_LILAC:
            self.mine_type_txt = 'mines_t02'
            mine_type_short = 't2'
            self.health_total = 25
            self.attack_power = MINE_T02_ATTACK_POWER

        if not Mine.sprite_images.get(self.mine_type):
            image_quality = '_md' if Settings.cell_size >= consts.CELL_SIZE_MIN_FOR_IM_MD else ''

            image = pg.image.load(resources.file_name_get(name='im_mine_', subname=mine_type_short,
                                                          quality=image_quality, num=1)).convert()
            image = pg.transform.smoothscale(image, Mine.size)
            image.set_colorkey(Color.BLACK)
            Mine.sprite_images[self.mine_type] = image
        else:
            image = Mine.sprite_images[self.mine_type]

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.health = self.health_total

        # Add mine to the active sprite list
        self.game.active_sprites.add(self)
        self.game.mines.add(self)

    @classmethod
    def init(cls):
        cls.size = lib_jp.Size(w=Settings.cell_size + cls.cell_added_size.w,
                               h=Settings.cell_size + cls.cell_added_size.h)
        cls._resize_images_on_cache()

    @classmethod
    def resize_images(cls):
        Mine.calculate_max_qty_on_board()
        if not Mine.sprite_images:
            return
        for key, image in Mine.sprite_images.items():
            if Mine.size.w != image.get_size()[0] or Mine.size.h != image.get_size()[1]:
                Mine.sprite_images[key] = pg.transform.smoothscale(image, Mine.size)

    @classmethod
    def calculate_max_qty_on_board(cls):
        cls.max_qty_on_board = 5 + ((Settings.screen_width * Settings.screen_height)
                                    // (Settings.cell_size * Settings.cell_size
                                        * consts.MAX_DIVIDER_MINES_ON_BOARD))
        if cls.max_qty_on_board > consts.MAX_MINES_ON_BOARD:
            cls.max_qty_on_board = consts.MAX_MINES_ON_BOARD

    @classmethod
    def create_some_random_pos(cls, n, mine_type, mine_list, game, probability_each=100):
        Actor.create_some_random_pos(actor_cls=cls, n=n, actor_type=mine_type,
                                     actor_list=mine_list, game=game,
                                     probability_each=probability_each)

    @classmethod
    def _resize_images_on_cache(cls):
        cls.calculate_max_qty_on_board()
        if not cls.sprite_images:
            return
        for key, image in cls.sprite_images.items():
            if cls.size.w != image.get_size()[0] or cls.size.h != image.get_size()[1]:
                cls.sprite_images[key] = pg.transform.smoothscale(image, cls.size)

    @staticmethod
    def create_some(mines, mine_list, game):
        for mine in mines:
            mine_list.add(Mine(mine[0], mine[1], mine[2], game))
