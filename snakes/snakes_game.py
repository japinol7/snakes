"""Module snakes_game."""
__author__ = 'Joan A. Pinol  (japinol)'
__all__ = ["Game"]

import logging

import pygame as pg

from snakes.bullets import BulletType
from snakes.colors import Color
from snakes.debug_info import DebugInfo
from snakes.help_info import HelpInfo
from snakes import levels
from snakes import lib_graphics_jp as libg_jp
from snakes.resources import Resource
from snakes.score_bars import ScoreBar
from snakes import screen
from snakes.scores import Scores
from snakes.settings import Settings
from snakes.snakes import Snake


logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Game:
    """Represents a Snakes game."""
    is_exit_game = False
    is_over = False
    is_first_game = True
    current_game = 0
    current_time = None
    active_sprites = None
    size = None
    screen = None
    screen_flags = None
    normal_screen_flags = None
    full_screen_flags = None

    def __init__(self, screen_width=None, screen_height=None,
                 is_full_screen=None, is_no_display_scaled=None,
                 cell_size=None, speed_pct=None, snake_body_len_start=None,
                 snake_body_len_max=None, score_to_win=None, portrait_mode=None):
        self.name = "Snakes v 1.01"
        self.name_short = "Snakes"
        self.start_time = None
        self.done = None
        self.snake1 = None
        self.snake2 = None
        self.winner = None
        self.current_level = None
        self.levels = []
        self.is_paused = False
        self.is_start_screen = True
        self.is_full_screen_switch = False
        self.is_help_screen = False
        self.is_exit_curr_game_confirm = False
        self.is_music_paused = False
        self.sound_effects = True
        self.show_fps = False
        self.show_grid = False
        self.clock = None
        self.score_bars = None
        self.help_info = None
        self.debug_info = None
        self.current_song = 0
        self.writen_info_game_over_to_file = False
        self.current_level_no = 0
        self.current_level_no_old = None
        self.screen_exit_current_game = None
        self.screen_game_over = None
        self.screen_pause = None
        self.screen_help = None

        Game.is_exit_game = False
        if Game.current_game > 0:
            Game.is_first_game = False

        if Game.is_first_game:
            # Calculate settings
            pg_display_info = pg.display.Info()
            Settings.display_start_width = pg_display_info.current_w
            Settings.display_start_height = pg_display_info.current_h
            Settings.calculate_settings(screen_width=screen_width,
                                        screen_height=screen_height, full_screen=is_full_screen,
                                        cell_size=cell_size, speed_pct=speed_pct,
                                        snake_body_len_start=snake_body_len_start,
                                        snake_body_len_max=snake_body_len_max,
                                        score_to_win=score_to_win, portrait_mode=portrait_mode)
            # Set screen to the settings configuration
            Game.size = [Settings.screen_width, Settings.screen_height]
            Game.full_screen_flags = pg.FULLSCREEN if is_no_display_scaled else pg.FULLSCREEN | pg.SCALED
            Game.normal_screen_flags = pg.SHOWN if is_no_display_scaled else pg.SHOWN | pg.SCALED
            Game.screen_flags = Game.full_screen_flags if Settings.is_full_screen else Game.normal_screen_flags
            Game.screen = pg.display.set_mode(Game.size, Game.screen_flags)
            # Load and render resources
            Resource.load_and_render_background_images()
            Resource.load_and_render_scorebar_images_and_txt()
            Resource.load_sound_resources()
            Resource.load_music_song(self.current_song)

            # Render characters in some colors to use it as a cache
            libg_jp.chars_render_text_tuple()

            # Initialize music
            pg.mixer.music.set_volume(0.7)
            pg.mixer.music.play(loops=-1)
            if self.is_music_paused:
                pg.mixer.music.pause()

        # Initialize screens
        self.screen_exit_current_game = screen.ExitCurrentGame(self)
        self.screen_help = screen.Help(self)
        self.screen_pause = screen.Pause(self)
        self.screen_game_over = screen.GameOver(self)

        # Initialize groups of sprites
        self.active_sprites = pg.sprite.Group()
        self.apples = pg.sprite.Group()
        self.mines = pg.sprite.Group()
        self.bats = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.cartridges = pg.sprite.Group()
        self.normal_items = pg.sprite.Group()
        self.rec_potions = pg.sprite.Group()
        self.snakes = pg.sprite.Group()
        self.snake_heads = pg.sprite.Group()

        # Initialize levels
        self.levels.extend([levels.Level_01(self),
                            levels.Level_02(self),
                            levels.Level_03(self),
                            levels.Level_04(self),
                            levels.Level_05(self),
                            levels.Level_06(self),
                            levels.Level_07(self),
                            levels.Level_others(self),
                            ])

    def set_is_exit_game(self, is_exit_game):
        Game.is_exit_game = is_exit_game

    def write_game_over_info_to_file(self):
        self.debug_info.print_debug_info(to_log_file=True)
        Scores.write_scores_to_file(self)
        self.writen_info_game_over_to_file = True

    def draw_grid(self):
        for x in range(0, Settings.screen_width, Settings.cell_size):
            pg.draw.line(Game.screen, Color.GRAY10, (x, Settings.screen_near_top),
                         (x, Settings.screen_height))
        for y in range(Settings.screen_near_top, Settings.screen_height, Settings.cell_size):
            pg.draw.line(Game.screen, Color.GRAY10, (0, y), (Settings.screen_width, y))

    def put_initial_actors_on_the_board(self):
        # Create snakes
        self.snake1 = Snake(color=1, x=Settings.snake1_position_ini[0],
                            y=Settings.snake1_position_ini[1], game=self)
        self.snake2 = Snake(color=2, x=Settings.snake2_position_ini[0],
                            y=Settings.snake2_position_ini[1], game=self)
        self.snake_heads.add(self.snake1)
        self.snake_heads.add(self.snake2)
        # For each snake, find out which snake body pieces are from another snakes
        self.snake1.fill_other_snakes_group()
        self.snake2.fill_other_snakes_group()
        # Start first level
        self.current_level = self.levels[self.current_level_no]
        self.current_level.start_up()

    def change_screen_level(self):
        self.current_level_no_old = self.current_level_no
        self.current_level_no += 1
        self.current_level.clean_up()
        self.current_level = self.levels[self.current_level.next_level]
        self.current_level.start_up()

    def update_screen(self):
        # Handle game screens
        if self.is_paused or self.is_full_screen_switch:
            self.screen_pause.start_up(is_full_screen_switch=self.is_full_screen_switch)
        if self.is_help_screen:
            self.screen_help.start_up()
        elif self.is_exit_curr_game_confirm:
            self.screen_exit_current_game.start_up()
        elif Game.is_over:
            self.screen_game_over.start_up()
            if not self.writen_info_game_over_to_file:
                self.write_game_over_info_to_file()
        else:
            if not Game.is_over:
                Game.screen.blit(Resource.images['background'], (0, 0))
            else:
                Game.screen.blit(Resource.images['bg_blue_t2'], (0, 0))
            Game.screen.blit(Resource.images['background_score_bar2'], (0, 0))
            Game.screen.blit(Resource.images['background_score_bar'], (0, 0))
            self.show_grid and self.draw_grid()
            # Update score bars
            self.score_bars.update(self.current_level_no, self.current_level_no_old)

            if self.current_level_no != self.current_level_no_old:
                self.current_level_no_old = self.current_level_no
            if not Game.is_over:
                # Draw active sprites
                self.active_sprites.draw(Game.screen)
                for sprite in self.bats:
                    sprite.draw_health()

        self.show_fps and pg.display.set_caption(f"{self.clock.get_fps():.2f}")

    def start(self):
        Game.is_exit_game = False
        Game.is_over = False
        Game.current_game += 1
        pg.display.set_caption(self.name_short)
        self.clock = pg.time.Clock()
        self.start_time = pg.time.get_ticks()

        # Put initial actors on the board and start moving the snakes to the right
        self.put_initial_actors_on_the_board()
        self.snake1.go_right()
        self.snake2.go_right()

        # Initialize score bars
        self.score_bars = ScoreBar(self.snake1, self.snake2, Game.screen)

        # Render text frequently used only if it is the first game
        if Game.is_first_game:
            Resource.render_text_frequently_used(self)

        self.help_info = HelpInfo()
        self.debug_info = DebugInfo(self.snake1, self.snake2, self)

        # Current game loop
        self.done = False
        while not self.done:
            self.current_time = pg.time.get_ticks()
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.is_exit_curr_game_confirm = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        self.is_paused = True
                    if event.key == pg.K_LEFT:
                        self.snake1.go_left()
                    elif event.key == pg.K_RIGHT:
                        self.snake1.go_right()
                    elif event.key == pg.K_UP:
                        self.snake1.go_up()
                    elif event.key == pg.K_DOWN:
                        self.snake1.go_down()
                    elif event.key == pg.K_KP4:
                        self.snake1.shot_bullet(bullet_type=BulletType.T1_LASER1)
                    elif event.key == pg.K_KP5:
                        self.snake1.shot_bullet(bullet_type=BulletType.T2_LASER2)
                    elif event.key == pg.K_KP1:
                        self.snake1.shot_bullet(bullet_type=BulletType.T3_PHOTONIC)
                    elif event.key == pg.K_KP2:
                        self.snake1.shot_bullet(bullet_type=BulletType.T4_NEUTRONIC)
                    elif event.key == pg.K_a:
                        self.snake2.go_left()
                    elif event.key == pg.K_d:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.debug_info.print_debug_info()
                        else:
                            self.snake2.go_right()
                    elif event.key == pg.K_w:
                        self.snake2.go_up()
                    elif event.key == pg.K_s:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.sound_effects = not self.sound_effects
                        else:
                            self.snake2.go_down()
                    elif event.key == pg.K_u:
                        self.snake2.shot_bullet(bullet_type=BulletType.T1_LASER1)
                    elif event.key == pg.K_i:
                        self.snake2.shot_bullet(bullet_type=BulletType.T2_LASER2)
                    elif event.key == pg.K_j:
                        self.snake2.shot_bullet(bullet_type=BulletType.T3_PHOTONIC)
                    elif event.key == pg.K_k:
                        self.snake2.shot_bullet(bullet_type=BulletType.T4_NEUTRONIC)
                    elif event.key == pg.K_m:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.is_music_paused = not self.is_music_paused
                            if self.is_music_paused:
                                pg.mixer.music.pause()
                            else:
                                pg.mixer.music.unpause()
                    elif event.key == pg.K_h:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.help_info.print_help_keys()
                            self.debug_info.print_help_keys()
                    elif event.key == pg.K_d:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.debug_info.print_debug_info()
                    elif event.key == pg.K_l:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.debug_info.print_debug_info(to_log_file=True)
                    elif event.key == pg.K_F1:
                        if not self.is_exit_curr_game_confirm:
                            self.is_help_screen = not self.is_help_screen
                    elif event.key == pg.K_g:
                        if pg.key.get_mods() & pg.KMOD_LCTRL and pg.key.get_mods() & pg.KMOD_RALT:
                            self.show_grid = not self.show_grid
                    elif event.key in (pg.K_KP_ENTER, pg.K_RETURN):
                        if pg.key.get_mods() & pg.KMOD_ALT:
                            self.is_paused = True
                            self.is_full_screen_switch = True
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_F5:
                        self.show_fps = not self.show_fps

            # Update sprites and level
            if not self.is_paused:
                self.active_sprites.update()
                # Pass level when all the apples on the board have been eaten
                if not self.apples:
                    self.change_screen_level()
            self.update_screen()
            self.clock.tick(Settings.fps)

            # Check if there is a winner or a tie
            if not self.snake1.is_alive and not self.snake2.is_alive:
                Game.is_over = True
                if self.snake1.stats['score'] > self.snake2.stats['score']:
                    self.winner = self.snake1
                elif self.snake2.stats['score'] > self.snake1.stats['score']:
                    self.winner = self.snake2
            if self.winner or Game.is_over:
                Game.is_over = True
            pg.display.flip()
