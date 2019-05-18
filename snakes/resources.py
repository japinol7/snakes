"""Module resources."""
__author__ = 'Joan A. Pinol  (japinol)'

import os

import pygame as pg

from snakes.colors import Color
from snakes import constants as consts
from snakes import lib_jp
from snakes import lib_graphics_jp as libg_jp
from snakes.settings import Settings


def file_name_get(name, subname='', num=None, subnum=None, quality='',
                  folder=consts.BITMAPS_FOLDER):
    return os.path.join(folder,
                        '%s%s%s%s.%s' % (consts.FILE_NAMES['%s%s' % (name, subname)][0],
                                         quality,
                                         num and '_%02i' % num or '',
                                         subnum and '_%02i' % subnum or '',
                                         consts.FILE_NAMES['%s%s' % (name, subname)][1])
                        )


class Resource:
    """Some resources used in the game that do not have their own class."""
    apple_hit_sound = None
    bat_hit_sound = None
    bat_scream_sound = None
    bullet_t1_sound = None
    bullet_t2_sound = None
    bullet_t3_sound = None
    bullet_t4_sound = None
    bullet_hit_sound = None
    collission_sound = None
    explosion_sound = None
    item_hit_sound = None
    mine_hit_sound = None
    weapon_empty_sound = None
    images = {}
    txt_surfaces = {'game_paused': None, 'snake1_wins': None, 'snake2_wins': None,
                    'game_tied': None, 'press_intro_to_continue': None, 'game_start': None,
                    'current_level_no': None,
                    }

    @classmethod
    def load_sound_resources(cls):
        cls.apple_hit_sound = pg.mixer.Sound(file_name_get(name='snd_apple_hit', folder=consts.SOUNDS_FOLDER))
        cls.bat_hit_sound = pg.mixer.Sound(file_name_get(name='snd_bat_hit', folder=consts.SOUNDS_FOLDER))
        cls.bat_scream_sound = pg.mixer.Sound(file_name_get(name='snd_bat_scream', folder=consts.SOUNDS_FOLDER))
        cls.bullet_t1_sound = pg.mixer.Sound(file_name_get(name='snd_bullet_t1', folder=consts.SOUNDS_FOLDER))
        cls.bullet_t2_sound = pg.mixer.Sound(file_name_get(name='snd_bullet_t2', folder=consts.SOUNDS_FOLDER))
        cls.bullet_t3_sound = pg.mixer.Sound(file_name_get(name='snd_bullet_t3', folder=consts.SOUNDS_FOLDER))
        cls.bullet_t4_sound = pg.mixer.Sound(file_name_get(name='snd_bullet_t4', folder=consts.SOUNDS_FOLDER))
        cls.bullet_hit_sound = pg.mixer.Sound(file_name_get(name='snd_explosion', folder=consts.SOUNDS_FOLDER))
        cls.collission_sound = pg.mixer.Sound(file_name_get(name='snd_collission', folder=consts.SOUNDS_FOLDER))
        cls.explosion_sound = pg.mixer.Sound(file_name_get(name='snd_explosion', folder=consts.SOUNDS_FOLDER))
        cls.item_hit_sound = pg.mixer.Sound(file_name_get(name='snd_apple_hit', folder=consts.SOUNDS_FOLDER))
        cls.mine_hit_sound = pg.mixer.Sound(file_name_get(name='snd_mine_hit', folder=consts.SOUNDS_FOLDER))
        cls.weapon_empty_sound = pg.mixer.Sound(file_name_get(name='snd_weapon_empty', folder=consts.SOUNDS_FOLDER))

    @classmethod
    def render_text_frequently_used(cls, game):
        # Render text
        libg_jp.render_text('– PAUSED –', Settings.screen_width // 2, Settings.screen_height // 2,
                            cls.txt_surfaces, 'game_paused', color=Color.RED,
                            size=int(148*Settings.font_pos_factor), align="center")
        libg_jp.render_text('– Press Escape to Exit this Game  –', Settings.screen_width // 2,
                            (Settings.screen_height // 2) - int(6 * Settings.font_pos_factor_t2),
                            cls.txt_surfaces, 'exit_current_game_confirm', color=Color.RED,
                            size=int(64*Settings.font_pos_factor_t2), align="center")
        libg_jp.render_text('– Press Enter to Continue –', Settings.screen_width // 2,
                            (Settings.screen_height // 2) + int(82 * Settings.font_pos_factor_t2),
                            cls.txt_surfaces, 'press_intro_to_continue', color=Color.RED,
                            size=int(64*Settings.font_pos_factor_t2), align="center")
        libg_jp.render_text("– GAME OVER. It's a Tie –", Settings.screen_width // 2,
                            Settings.screen_height // 2,
                            cls.txt_surfaces, 'game_tied', color=Color.RED,
                            size=int(80*Settings.font_pos_factor), align="center")
        for snake_tuple in ((game.snake1.color, 'snake1_wins'), (game.snake2.color, 'snake2_wins')):
            libg_jp.render_text(f'– {lib_jp.map_color_num_to_name_txt(snake_tuple[0])} Snake Wins! –',
                                Settings.screen_width / 2, Settings.screen_height / 2,
                                cls.txt_surfaces, f'{snake_tuple[1]}', color=Color.RED,
                                size=int(80*Settings.font_pos_factor), align="center")

    @classmethod
    def load_and_render_background_images(cls):
        # Load and render background images and effects.
        img = pg.Surface((Settings.screen_width, Settings.screen_height)).convert_alpha()
        img.fill((0, 0, 0, 55))
        cls.images['dim_screen'] = img

        img = pg.image.load(file_name_get(name='im_background', subname='')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_height))
        cls.images['background'] = img

        img = pg.image.load(file_name_get(name='im_bg_score_bar', subname='')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width,
                                             int(Settings.screen_near_top // 1.9)))
        cls.images['background_score_bar'] = img

        img = pg.image.load(file_name_get(name='im_bg_score_bar2', subname='')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_near_top))
        cls.images['background_score_bar2'] = img

        img = pg.image.load(file_name_get(name='im_bg_blue_', subname='t1')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_height))
        cls.images['bg_blue_t1'] = img

        img = pg.image.load(file_name_get(name='im_bg_blue_', subname='t2')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_height))
        cls.images['bg_blue_t2'] = img

        img = pg.image.load(file_name_get(name='im_bg_black_', subname='t1')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_height))
        cls.images['bg_black_t1'] = img

        img = pg.image.load(file_name_get(name=Settings.im_screen_help,
                                          subname='', num=1)).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width_adjusted,
                                             Settings.screen_height_adjusted))
        cls.images['screen_help'] = img

        img = pg.image.load(file_name_get(name=Settings.im_bg_start_game,
                                          subname='')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width_adjusted,
                                             Settings.screen_height_adjusted))
        cls.images['screen_start'] = img

        img = pg.image.load(file_name_get(name='im_help_key', subname='')).convert()
        img = pg.transform.smoothscale(img, (int((Settings.help_key_size.w)
                                                 * Settings.font_pos_factor_t2),
                                             int(Settings.help_key_size.h
                                                 * Settings.font_pos_factor_t2)))
        cls.images['help_key'] = img

        img = pg.image.load(file_name_get(name='im_logo_japinol', subname='')).convert()
        img = pg.transform.smoothscale(img, (int((Settings.logo_jp_std_size.w)
                                                 * Settings.font_pos_factor_t2),
                                             int(Settings.logo_jp_std_size.h
                                                 * Settings.font_pos_factor_t2)))
        cls.images['logo_jp'] = img

    @classmethod
    def load_and_render_scorebar_images_and_txt(cls):
        img = pg.image.load(file_name_get(name='im_apple_', subname='t1',
                                          quality='_md', num=1)).convert()
        img = pg.transform.smoothscale(img, Settings.score_pos_apples_size)
        img.set_colorkey(Color.BLACK)
        cls.images['sb_apples_title'] = img

        bullets_stats = ['sb_bullets_t1', 'sb_bullets_t2', 'sb_bullets_t3', 'sb_bullets_t4']
        for bullet_stats in bullets_stats:
            img = pg.image.load(file_name_get(name='im_bullet_', subname=bullet_stats[-2:],
                                              quality='_md', num=1)).convert()
            img = pg.transform.smoothscale(img, Settings.score_pos_bullets_size)
            img.set_colorkey(Color.BLACK)
            cls.images[bullet_stats] = img

        libg_jp.render_text('L:', Settings.score_pos_lives1[0], Settings.screen_bar_near_top,
                            cls.txt_surfaces, 'sb_lives_title1', color=Color.GREEN)
        libg_jp.render_text('L:', Settings.score_pos_lives2[0], Settings.screen_bar_near_top,
                            cls.txt_surfaces, 'sb_lives_title2', color=Color.YELLOW)
        libg_jp.render_text('S:', Settings.score_pos_score1[0], Settings.screen_bar_near_top,
                            cls.txt_surfaces, 'sb_score_title1', color=Color.GREEN)
        libg_jp.render_text('S:', Settings.score_pos_score2[0], Settings.screen_bar_near_top,
                            cls.txt_surfaces, 'sb_score_title2', color=Color.YELLOW)
        libg_jp.render_text('#', Settings.score_pos_level[0], Settings.screen_bar_near_top,
                            cls.txt_surfaces, 'sb_current_level_title', color=Color.CYAN)

    @staticmethod
    def load_music_song(current_song):
        pg.mixer.music.load(os.path.join(consts.MUSIC_FOLDER, consts.MUSIC_BOX[current_song]))
