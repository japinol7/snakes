"""Module score_bars."""
__author__ = 'Joan A. Pinol  (japinol)'

from snakes.colors import Color
from snakes import lib_graphics_jp as libg_jp
from snakes.resources import Resource
from snakes.settings import Settings
from snakes import snakes


class ScoreBar:
    """Represents a score bar."""

    def __init__(self, snake1, snake2, screen):
        self.snake1 = snake1
        self.snake2 = snake2
        self.screen = screen
        self.current_level_no = None
        self.current_level_no_old = None

    def draw_chars_render_text(self, text, x, y, color=Color.YELLOW):
        libg_jp.draw_text_rendered(text, x, y, self.screen, color)

    def render_stats_if_necessary(self, x1, x2, y, stats_name, size=None):
        # Snake1 stat
        if not size:
            size = Settings.font_size2
        libg_jp.draw_text_rendered(text=f'{self.snake1.stats[stats_name]}',
                                        x=x1, y=y, screen=self.screen, color=Color.GREEN)
        if self.snake1.stats[stats_name] != self.snake1.stats_old[stats_name]:
            self.snake1.stats_old[stats_name] = self.snake1.stats[stats_name]

        # Snake2 stat
        libg_jp.draw_text_rendered(text=f'{self.snake2.stats[stats_name]}',
                                        x=x2, y=y, screen=self.screen, color=Color.YELLOW)
        if self.snake2.stats[stats_name] != self.snake2.stats_old[stats_name]:
            self.snake2.stats_old[stats_name] = self.snake2.stats[stats_name]

    def draw_stats(self):
        # Draw snake1 score titles
        self.screen.blit(*Resource.txt_surfaces['sb_current_level_title'])
        self.screen.blit(*Resource.txt_surfaces['sb_lives_title1'])
        self.screen.blit(Resource.images['sb_apples_title'],
                         (Settings.score_pos_apples1[0], Settings.score_pos_apples_y))
        self.screen.blit(*Resource.txt_surfaces['sb_score_title1'])

        bullet_pos_x = 150
        bullets_stats = ['sb_bullets_t1', 'sb_bullets_t2', 'sb_bullets_t3', 'sb_bullets_t4']
        for bullet_stats in bullets_stats:
            self.screen.blit(Resource.images[bullet_stats],
                             (bullet_pos_x * Settings.font_pos_factor,
                              int(Settings.score_pos_bullets_size[1]
                                  + Settings.score_pos_bullets_y)))
            bullet_pos_x += 85

        # Draw snake2 score titles
        self.screen.blit(*Resource.txt_surfaces['sb_lives_title2'])
        self.screen.blit(Resource.images['sb_apples_title'], (Settings.score_pos_apples2[0],
                                                              Settings.score_pos_apples_y))
        self.screen.blit(*Resource.txt_surfaces['sb_score_title2'])

        bullet_pos_x = 785
        bullets_stats = ['sb_bullets_t1', 'sb_bullets_t2', 'sb_bullets_t3', 'sb_bullets_t4']
        for bullet_stats in bullets_stats:
            self.screen.blit(Resource.images[bullet_stats],
                             (bullet_pos_x * Settings.font_pos_factor,
                              int(Settings.score_pos_bullets_size[1] + Settings.score_pos_bullets_y)))
            bullet_pos_x += 85

        # Draw score stats and render them if needed
        self.render_stats_if_necessary(Settings.score_pos_lives1[1], Settings.score_pos_lives2[1],
                                       Settings.screen_bar_near_top, 'lives')
        self.render_stats_if_necessary(Settings.score_pos_apples1[1], Settings.score_pos_apples2[1],
                                       Settings.screen_bar_near_top, 'apples')
        self.render_stats_if_necessary(Settings.score_pos_score1[1], Settings.score_pos_score2[1],
                                       Settings.screen_bar_near_top, 'score')

        bullet_pos_x = 179
        bullets_stats = ['bullets_t01', 'bullets_t02', 'bullets_t03', 'bullets_t04']
        for bullet_stats in bullets_stats:
            self.render_stats_if_necessary(bullet_pos_x * Settings.font_pos_factor,
                                           (bullet_pos_x + 638) * Settings.font_pos_factor,
                                           Settings.score_pos_bullets_y + 10 * Settings.font_pos_factor,
                                           bullet_stats)
            bullet_pos_x += 83

        libg_jp.draw_text_rendered(text=f'{self.current_level_no + 1}',
                                        x=Settings.score_pos_level[1],
                                        y=Settings.screen_bar_near_top,
                                        screen=self.screen, color=Color.CYAN)

    def update(self, current_level_no, current_level_no_old):
        self.current_level_no = current_level_no
        self.current_level_no_old = current_level_no_old
        libg_jp.draw_bar_graphic(self.screen, amount_pct=self.snake1.stats['health'] / snakes.SNAKE_HEALTH,
                                 x=Settings.score_pos_health1_xy[0], y=Settings.score_pos_health1_xy[1],
                                 bar_width=Settings.score_pos_health_size[0],
                                 bar_height=Settings.score_pos_health_size[1])
        libg_jp.draw_bar_graphic(self.screen, amount_pct=self.snake2.stats['health'] / snakes.SNAKE_HEALTH,
                                 x=Settings.score_pos_health2_xy[0], y=Settings.score_pos_health2_xy[1],
                                 bar_width=Settings.score_pos_health_size[0],
                                 bar_height=Settings.score_pos_health_size[1])

        libg_jp.draw_bar_graphic(self.screen, amount_pct=self.snake1.stats['power'] / snakes.SNAKE_POWER,
                                 x=Settings.score_pos_health1_xy[0],
                                 y=Settings.score_pos_health1_xy[1] + 39 * Settings.font_pos_factor,
                                 bar_width=Settings.score_pos_power_size[0],
                                 bar_height=Settings.score_pos_power_size[1],
                                 color_max=Color.BLUE, color_med=Color.BLUE_VIOLET, color_min=Color.CYAN)
        libg_jp.draw_bar_graphic(self.screen, amount_pct=self.snake2.stats['power'] / snakes.SNAKE_POWER,
                                 x=Settings.score_pos_health2_xy[0],
                                 y=Settings.score_pos_health2_xy[1] + 39 * Settings.font_pos_factor,
                                 bar_width=Settings.score_pos_power_size[0],
                                 bar_height=Settings.score_pos_power_size[1],
                                 color_max=Color.BLUE, color_med=Color.BLUE_VIOLET, color_min=Color.CYAN)
        self.draw_stats()
