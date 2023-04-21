"""Module screen."""
__author__ = 'Joan A. Pinol  (japinol)'

from snakes.colors import Color
from snakes import lib_graphics_jp as libg_jp
from snakes.resources import Resource
from snakes.settings import Settings
from snakes.tools.screen import screen


class ExitCurrentGame(screen.ExitCurrentGame):

    def _draw(self):
        super()._draw()
        self.game.screen.blit(Resource.images['bg_blue_t1'], (0, 0))
        self.game.screen.blit(*Resource.txt_surfaces['exit_current_game_confirm'])
        self.game.screen.blit(*Resource.txt_surfaces['press_intro_to_continue'])


class GameOver(screen.GameOver):

    def _draw(self):
        super()._draw()
        if self.game.is_over and not self.game.winner:
            self.game.screen.blit(*Resource.txt_surfaces['game_tied'])
        else:
            self.game.screen.blit(*Resource.txt_surfaces[f'snake{self.game.winner.color}_wins'])
        self.game.screen.blit(*Resource.txt_surfaces['press_intro_to_continue'])


class Pause(screen.Pause):

    def _draw(self):
        super()._draw()
        if self.is_full_screen_switch:
            self.game.screen.blit(self.background_screenshot, (0, 0))
        self.game.screen.blit(*Resource.txt_surfaces['game_paused'])
        self.game.screen.blit(Resource.images['dim_screen'], (0, 0))


class Help(screen.Help):

    def _draw(self):
        super()._draw()
        self.game.screen.blit(Resource.images['bg_blue_t1'], (0, 0))
        self.game.screen.blit(Resource.images['screen_help'],
                              (Settings.screen_width // 2 - Resource.images['screen_help'].get_width() // 2,
                               Settings.screen_height // 2 - Resource.images['screen_help'].get_height() // 2))


class StartGame(screen.StartGame):

    def __init__(self, game):
        super().__init__(game)

        libg_jp.render_text('– Press Enter to Start –', Settings.screen_width // 2,
                            114 * Settings.font_pos_factor_t2 + Settings.screen_height // 2,
                            Resource.txt_surfaces, 'game_start', color=Color.RED,
                            size=int(96*Settings.font_pos_factor_t2), align="center")

    def _draw(self):
        super()._draw()
        self.game.screen.blit(Resource.images['bg_black_t1'], (0, 0))
        self.game.screen.blit(Resource.images['screen_start'],
                              (Settings.screen_width // 2 - Resource.images['screen_start'].get_width() // 2, 0))
        self.game.screen.blit(Resource.images['help_key'],
                              (50 * Settings.font_pos_factor,
                              Settings.screen_height - Resource.images['help_key'].get_height()
                              - 35 * Settings.font_pos_factor))
        self.game.screen.blit(Resource.images['logo_jp'],
                              (Settings.screen_width - Resource.images['logo_jp'].get_width()
                              - 31 * Settings.font_pos_factor,
                              Settings.screen_height - Resource.images['logo_jp'].get_height()
                              - 31 * Settings.font_pos_factor))
        self.game.screen.blit(*Resource.txt_surfaces['game_start'])
