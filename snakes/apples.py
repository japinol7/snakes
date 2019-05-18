"""Module apples."""
__author__ = 'Joan A. Pinol  (japinol)'

from enum import Enum
import pygame as pg

from snakes.actors import Actor, ActorType
from snakes.colors import Color
from snakes import constants as consts
from snakes import lib_jp
from snakes import resources
from snakes.settings import Settings


class AppleType(Enum):
    """Apple types."""
    T1_RED = 1
    T2_GREEN = 2
    T3_YELLOW = 3


class Apple(pg.sprite.Sprite):
    """Represents an apple."""
    actor_type = ActorType.APPLE
    cell_added_size = lib_jp.Size(w=5, h=5)  # Added size to the defined cell size.
    size = None
    sprite_images = {}
    max_qty_on_board = None

    def __init__(self, x, y, apple_type, game):
        super().__init__()
        self.images_sprite_no = 1
        self.frame = 0
        self.rect = None
        self.apple_type = apple_type
        self.game = game
        self.apple_type_txt = None

        if self.apple_type == AppleType.T1_RED:
            self.apple_type_txt = 'apples_t01'
            apple_type_short = 't1'
        elif self.apple_type == AppleType.T2_GREEN:
            self.apple_type_txt = 'apples_t02'
            apple_type_short = 't2'
        elif self.apple_type == AppleType.T3_YELLOW:
            self.apple_type_txt = 'apples_t03'
            apple_type_short = 't3'

        if not Apple.sprite_images.get(self.apple_type):
            image_quality = '_md' if Settings.cell_size >= consts.CELL_SIZE_MIN_FOR_IM_MD else ''
            image = pg.image.load(resources.file_name_get(name='im_apple_', subname=apple_type_short,
                                                          quality=image_quality, num=1)).convert()
            image = pg.transform.smoothscale(image, Apple.size)
            image.set_colorkey(Color.BLACK)
            Apple.sprite_images[self.apple_type] = image
        else:
            image = Apple.sprite_images[self.apple_type]

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Add apple to the active sprite list
        self.game.active_sprites.add(self)
        self.game.apples.add(self)
        self.game.normal_items.add(self)

    @classmethod
    def init(cls):
        cls.size = lib_jp.Size(w=Settings.cell_size + cls.cell_added_size.w,
                               h=Settings.cell_size + cls.cell_added_size.h)
        cls._resize_images_on_cache()

    @classmethod
    def calculate_max_qty_on_board(cls):
        cls.max_qty_on_board = 5 + ((Settings.screen_width * Settings.screen_height)
                                    // (Settings.cell_size * Settings.cell_size
                                        * consts.MAX_DIVIDER_APPLES_ON_BOARD))
        if cls.max_qty_on_board > consts.MAX_APPLES_ON_BOARD:
            cls.max_qty_on_board = consts.MAX_APPLES_ON_BOARD

    @classmethod
    def create_some_random_pos(cls, n, apple_type, apple_list, game, probability_each=100):
        Actor.create_some_random_pos(actor_cls=cls, n=n, actor_type=apple_type,
                                     actor_list=apple_list, game=game,
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
    def create_some(apples, apple_list, game):
        for apple in apples:
            apple_list.add(Apple(apple[0], apple[1], apple[2], game))
