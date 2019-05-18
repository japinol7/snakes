"""Module constants."""
__author__ = 'Joan A. Pinol  (japinol)'

import os
import sys


CELL_SIZE_MIN_FOR_IM_MD = 19       # Minimum cell size for image in medium resolution

MAX_APPLES_ON_BOARD = 18
MAX_MINES_ON_BOARD = 30
MAX_BATS_ON_BOARD = 7
MAX_DIVIDER_APPLES_ON_BOARD = 186
MAX_DIVIDER_MINES_ON_BOARD = 130

# Directions for moving actors
DIRECTION_LEFT = 1
DIRECTION_RIGHT = 2
DIRECTION_UP = 3
DIRECTION_DOWN = 4
DIRECTION_RIP = 5    # Special direction to use when a player character is dead

LOG_FILE = os.path.join('files', 'log.txt')
SCORES_FILE = os.path.join('files', 'scores.txt')


# If the code is frozen, use this path:
if getattr(sys, 'frozen', False):
    CURRENT_PATH = sys._MEIPASS
    BITMAPS_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'img')
    SOUNDS_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'snd')
    MUSIC_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'music')
    FONT_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'data')
    FONT_DEFAULT_NAME = os.path.join(FONT_FOLDER, 'sans.ttf')
else:
    BITMAPS_FOLDER = os.path.join('assets', 'img')
    SOUNDS_FOLDER = os.path.join('assets', 'snd')
    MUSIC_FOLDER = os.path.join('assets', 'music')
    FONT_DEFAULT_NAME = os.path.join('assets', 'data', 'sans.ttf')


MUSIC_BOX = ('action_song__192b.mp3',
             )

FILE_NAMES = {
                'im_snake_head': ('im_snake_head', 'png'),
                'im_snake_body': ('im_snake_body', 'png'),
                'im_snake_tail': ('im_snake_tail', 'png'),
                'im_apple_t1': ('im_apple_t1', 'png'),
                'im_apple_t2': ('im_apple_t2', 'png'),
                'im_apple_t3': ('im_apple_t3', 'png'),
                'im_mine_t1': ('im_mine_t1', 'png'),
                'im_mine_t2': ('im_mine_t2', 'png'),
                'im_bat_t1': ('im_bat_t1', 'png'),
                'im_bat_t2': ('im_bat_t2', 'png'),
                'im_bat_t3': ('im_bat_t3', 'png'),
                'im_bullet_t1': ('im_bullet_t1', 'png'),
                'im_bullet_t2': ('im_bullet_t2', 'png'),
                'im_bullet_t3': ('im_bullet_t3', 'png'),
                'im_bullet_t4': ('im_bullet_t4', 'png'),
                'im_cartridge_t1': ('im_cartridge_t1', 'png'),
                'im_cartridge_t2': ('im_cartridge_t2', 'png'),
                'im_cartridge_t3': ('im_cartridge_t3', 'png'),
                'im_cartridge_t4': ('im_cartridge_t4', 'png'),
                'im_rec_potion_t1': ('im_health_rec_t1', 'png'),
                'im_rec_potion_t2': ('im_power_rec_t1', 'png'),
                'im_bg_start_game': ('bg_start_game', 'png'),
                'im_bg_start_game_vertical': ('bg_start_game_vert', 'png'),
                'im_background': ('background', 'png'),
                'im_bg_score_bar': ('bg_score_bar', 'png'),
                'im_bg_score_bar2': ('bg_score_bar2', 'png'),
                'im_screen_help': ('screen_help', 'png'),
                'im_screen_help_vertical': ('screen_help_vert', 'png'),
                'im_logo_japinol': ('logo_japinol', 'png'),
                'im_help_key': ('help_key', 'png'),
                'im_bg_blue_t1': ('bg_blue_t1', 'png'),
                'im_bg_blue_t2': ('bg_blue_t2', 'png'),
                'im_bg_black_t1': ('bg_black_t1', 'png'),
                'snd_apple_hit': ('apple_hit', 'wav'),
                'snd_collission': ('collision', 'wav'),
                'snd_bat_hit': ('bat_hit', 'wav'),
                'snd_bat_scream': ('bat_scream', 'wav'),
                'snd_bullet_t1': ('bullet_t1', 'wav'),
                'snd_bullet_t2': ('bullet_t2', 'wav'),
                'snd_bullet_t3': ('bullet_t3', 'wav'),
                'snd_bullet_t4': ('bullet_t4', 'wav'),
                'snd_weapon_empty': ('weapon_empty', 'wav'),
                'snd_explosion': ('explosion', 'wav'),
                'snd_mine_hit': ('mine_hit', 'wav'),
            }
