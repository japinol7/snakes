"""Module settings."""
__author__ = 'Joan A. Pinol  (japinol)'

from snakes import lib_jp


SCREEN_MAX_WIDTH = 1920
SCREEN_MAX_HEIGHT = 1080
SCREEN_MIN_WIDTH = 400
SCREEN_MIN_HEIGHT = 200

CELL_DEFAULT_SIZE = 14
CELL_MAX_SIZE = 30
CELL_MIN_SIZE = 4

FPS_DEFAULT = 32
FPS_MIN = 12
FPS_MAX = 500

SCORE_MAX_TO_WIN = 999999
SCORE_MIN_TO_WIN = 1


class Settings:
    """Settings of the game."""
    screen_width = None
    screen_height = None
    screen_aspect_ratio = None
    screen_aspect_ratio_portrait = None
    screen_height_adjusted = None
    screen_width_adjusted = None
    display_start_width = None    # max. width of the user's initial display mode
    display_start_height = None   # max. height of the user's initial display mode
    portrait_mode = None
    cell_size = None
    fps = None
    fps_paused = None
    speed_pct = None
    is_full_screen = False
    im_screen_help = None
    im_bg_start_game = None
    score_to_win = None
    snake_body_len_start = None
    snake_body_len_max = None
    screen_near_top = None
    screen_near_bottom = None
    screen_near_right = None
    grid_width = None
    grid_height = None
    screen_bar_near_top = None
    snake1_position_ini = None
    snake2_position_ini = None
    sprite_health_bar_pos_rel = None   # Relative position for sprite health bar
    sprite_health_bar_size = None
    font_size1 = None
    font_size2 = None
    font_spc_btn_chars1 = None
    font_spc_btn_chars2 = None
    # scores tuple with label and value x positions
    score_pos_lives1 = None
    score_pos_apples1 = None
    score_pos_score1 = None
    score_pos_level = None
    score_pos_lives2 = None
    score_pos_apples2 = None
    score_pos_score2 = None
    score_pos_health1_xy = None
    score_pos_health2_xy = None
    score_pos_health_size = None
    score_pos_power_size = None
    font_pos_factor = None
    font_pos_factor_t2 = None
    score_pos_apples_y = None
    score_pos_apples_size = None
    score_pos_bullets_y = None
    score_pos_bullets_size = None
    logo_jp_std_size = None
    help_key_size = None

    @classmethod
    def clean(cls):
        cls.screen_width = 1260
        cls.screen_height = 903
        cls.screen_aspect_ratio = cls.screen_width / cls.screen_height
        cls.screen_aspect_ratio_portrait = cls.screen_height / cls.screen_width
        cls.screen_height_adjusted = None
        cls.screen_width_adjusted = None
        cls.portrait_mode = False
        cls.cell_size = CELL_DEFAULT_SIZE
        cls.cell_size_ratio = cls.screen_width * cls.screen_height / CELL_DEFAULT_SIZE
        cls.fps = FPS_DEFAULT
        cls.fps_paused = 14
        cls.speed_pct = 100
        cls.is_full_screen = False
        cls.im_screen_help = 'im_screen_help'
        cls.im_bg_start_game = 'im_bg_start_game'
        cls.snake_body_len_start = 5
        cls.snake_body_len_max = 700
        cls.score_to_win = SCORE_MAX_TO_WIN
        cls.screen_near_top = None
        cls.screen_near_bottom = None
        cls.screen_near_right = None
        cls.grid_width = None
        cls.grid_height = None
        cls.screen_bar_near_top = None
        cls.snake1_position_ini = None
        cls.snake2_position_ini = None
        cls.font_size1 = None
        cls.font_size2 = None
        cls.font_spc_btn_chars1 = None
        cls.font_spc_btn_chars2 = None
        # scores tuple with label and value x positions
        cls.score_pos_health1_xy = [15, 15]
        cls.score_pos_lives1 = [150, 190]
        cls.score_pos_apples1 = [240, 273]
        cls.score_pos_score1 = [340, 375]
        cls.score_pos_level = [498, 538]
        cls.score_pos_health2_xy = [644, 15]
        cls.score_pos_lives2 = [784, 824]
        cls.score_pos_apples2 = [884, 917]
        cls.score_pos_score2 = [984, 1021]
        cls.score_pos_health_size = [100, 15]
        cls.score_pos_power_size = cls.score_pos_health_size
        cls.font_pos_factor = 1                   # position or size factor for some text to render
        cls.font_pos_factor_t2 = 1                # position or size factor for some other text to render
        cls.score_pos_apples_y = None
        cls.score_pos_apples_size = [18, 18]
        cls.score_pos_bullets_size = [16, 16]
        cls.score_pos_bullets_y = None
        cls.logo_jp_std_size = lib_jp.Size(w=244, h=55)
        cls.help_key_size = lib_jp.Size(w=218, h=57)

    @classmethod
    def calculate_settings(cls, screen_width=None, screen_height=None,
                           full_screen=None, cell_size=None, speed_pct=None,
                           snake_body_len_start=None, snake_body_len_max=None,
                           score_to_win=None, portrait_mode=None):

        def _calculate_max_screen_size(screen_width, screen_height):
            screen_max_width = min([SCREEN_MAX_WIDTH, cls.display_start_width])
            screen_max_height = min([SCREEN_MAX_HEIGHT, cls.display_start_height])
            if screen_width and screen_width.isdigit():
                cls.screen_width = int(screen_width)
                if cls.screen_width < SCREEN_MIN_WIDTH:
                    cls.screen_width = SCREEN_MIN_WIDTH
                elif cls.screen_width > screen_max_width:
                    cls.screen_width = screen_max_width
                if not screen_height or not screen_height.isdigit():
                    cls.screen_height = int(cls.screen_width / cls.screen_aspect_ratio)
                    if cls.screen_height > screen_max_height:
                        cls.screen_height = screen_max_height
            if screen_height and screen_height.isdigit():
                cls.screen_height = int(screen_height)
                if cls.screen_height < SCREEN_MIN_HEIGHT:
                    cls.screen_height = SCREEN_MIN_HEIGHT
                elif cls.screen_height > screen_max_height:
                    cls.screen_height = screen_max_height
                    if not cls.portrait_mode:
                        cls.screen_width = int(cls.screen_height * cls.screen_aspect_ratio)
                    else:
                        cls.screen_width = int(cls.screen_height / cls.screen_aspect_ratio)
                if not screen_width or not screen_width.isdigit():
                    cls.screen_width = int(cls.screen_height * cls.screen_aspect_ratio)

        cls.clean()
        # Define screen values to resize the screen and images if necessary
        _calculate_max_screen_size(screen_width, screen_height)
        if portrait_mode:
            cls.portrait_mode = True
            if cls.screen_height < cls.screen_width:
                cls.screen_width, cls.screen_height = cls.screen_height, cls.screen_width
                _calculate_max_screen_size(str(cls.screen_width), str(cls.screen_height))
        # Examine portrait mode
        if cls.screen_width < cls.screen_height:
            cls.im_screen_help = 'im_screen_help_vertical'
            cls.im_bg_start_game = 'im_bg_start_game_vertical'
            cls.screen_aspect_ratio = cls.screen_aspect_ratio_portrait
            cls.screen_height_adjusted = cls.screen_width
            cls.screen_width_adjusted = int(cls.screen_width * cls.screen_aspect_ratio_portrait)
        else:
            cls.screen_width_adjusted = int(cls.screen_height * cls.screen_aspect_ratio)
            cls.screen_height_adjusted = cls.screen_height
        # Resizes adjusted screen values for images if they are to high
        if cls.screen_height_adjusted > cls.screen_height:
            cls.screen_width_adjusted -= cls.screen_height_adjusted - cls.screen_height
            cls.screen_height_adjusted -= cls.screen_height_adjusted - cls.screen_height
        if cls.screen_width_adjusted > cls.screen_width:
            cls.screen_height_adjusted -= cls.screen_width_adjusted - cls.screen_width
            cls.screen_width_adjusted -= cls.screen_width_adjusted - cls.screen_width
        # Set full screen or windowed screen
        cls.is_full_screen = True if full_screen else False
        # Resizes cell
        if cell_size and cell_size.isdigit():
            cls.cell_size = int(cell_size)
            if cls.cell_size < CELL_MIN_SIZE:
                cls.cell_size = CELL_MIN_SIZE
            elif cls.cell_size > CELL_MAX_SIZE:
                cls.cell_size = CELL_MAX_SIZE
        else:
            cls.cell_size = round(cls.screen_width * cls.screen_height / cls.cell_size_ratio)
            if cls.cell_size > CELL_DEFAULT_SIZE * 1.15:
                cls.cell_size = round(CELL_DEFAULT_SIZE * 1.15)
            elif cls.cell_size < CELL_DEFAULT_SIZE / 3.9:
                cls.cell_size = round(CELL_DEFAULT_SIZE / 2.1)
            elif cls.cell_size < CELL_DEFAULT_SIZE / 2:
                cls.cell_size = round(CELL_DEFAULT_SIZE / 1.9)
        # Set fps
        if speed_pct and speed_pct.isdigit():
            cls.speed_pct = speed_pct
            cls.fps = int(cls.fps * int(speed_pct) / 100)
            if cls.fps < FPS_MIN:
                cls.fps = FPS_MIN
            elif cls.fps > FPS_MAX:
                cls.fps = FPS_MAX
        # Set snake body initial attributes
        if snake_body_len_start and snake_body_len_start.isdigit():
            cls.snake_body_len_start = int(snake_body_len_start)
            if cls.snake_body_len_start < 1:
                cls.snake_body_len_start = 1
        if snake_body_len_max and snake_body_len_max.isdigit():
            cls.snake_body_len_max = int(snake_body_len_max)
            if cls.snake_body_len_max < cls.snake_body_len_start:
                cls.snake_body_len_max = cls.snake_body_len_start + 1
        # Set score to win
        if score_to_win and score_to_win.isdigit():
            cls.score_to_win = int(score_to_win)
            if cls.score_to_win < SCORE_MIN_TO_WIN:
                cls.score_to_win = SCORE_MIN_TO_WIN
            elif cls.score_to_win > SCORE_MAX_TO_WIN:
                cls.score_to_win = SCORE_MAX_TO_WIN
        # Set positions for images and text
        cls.screen_near_bottom = cls.screen_height - cls.cell_size + 1
        cls.screen_near_right = cls.screen_width - cls.cell_size + 1
        cls.grid_width = cls.screen_width // cls.cell_size
        cls.grid_height = cls.screen_height // cls.cell_size
        cls.screen_bar_near_top = 10

        cls.snake1_position_ini = (cls.cell_size * 14, cls.screen_height // 5)
        cls.snake2_position_ini = (cls.cell_size * 14,
                                   cls.screen_height // 5 + cls.cell_size * 5)

        # Font sizes for scores, etc
        cls.font_size1 = 24
        cls.font_size2 = 36
        cls.font_spc_btn_chars1 = 15
        cls.font_spc_btn_chars2 = 21
        cls.score_pos_apples_y = cls.screen_bar_near_top + 5
        cls.score_pos_bullets_y = cls.screen_bar_near_top + 29

        # Adapt size of images and text for some tested scenarios
        if cls.screen_width <= SCREEN_MAX_WIDTH:
            if cls.screen_width < 341:
                cls.font_pos_factor = 0.29
            elif cls.screen_width < 381:
                cls.font_pos_factor = 0.33
            elif cls.screen_width < 420:
                cls.font_pos_factor = 0.35
            elif cls.screen_width < 491:
                cls.font_pos_factor = 0.38
            elif cls.screen_width < 540:
                cls.font_pos_factor = 0.44
            elif cls.screen_width < 580:
                cls.font_pos_factor = 0.48
            elif cls.screen_width < 650:
                cls.font_pos_factor = 0.51
            elif cls.screen_width < 780:
                cls.font_pos_factor = 0.59
            elif cls.screen_width < 860:
                cls.font_pos_factor = 0.67
            elif cls.screen_width < 920:
                cls.font_pos_factor = 0.78
            elif cls.screen_width < 1025:
                cls.font_pos_factor = 0.84
            elif cls.screen_width < 1151:
                cls.font_pos_factor = 0.904
            elif cls.screen_width < 1201:
                cls.font_pos_factor = 0.91
            else:
                cls.font_pos_factor = 1.05

            cls.font_pos_factor_t2 = cls.font_pos_factor
            if not cls.portrait_mode and cls.screen_width / cls.screen_height >= 2.5:
                cls.font_pos_factor_t2 = 0.55

            cls.screen_bar_near_top = int(cls.screen_bar_near_top * cls.font_pos_factor)

            # Set score text and images positions and size
            cls.font_size1 = int(cls.font_size1 * cls.font_pos_factor)
            cls.font_size2 = int(cls.font_size2 * cls.font_pos_factor)
            cls.font_spc_btn_chars1 = int(cls.font_spc_btn_chars1 * cls.font_pos_factor)
            cls.font_spc_btn_chars2 = int(cls.font_spc_btn_chars2 * cls.font_pos_factor)
            cls.score_pos_lives1[0] = int(cls.score_pos_lives1[0] * cls.font_pos_factor)
            cls.score_pos_apples1[0] = int(cls.score_pos_apples1[0] * cls.font_pos_factor)
            cls.score_pos_score1[0] = int(cls.score_pos_score1[0] * cls.font_pos_factor)
            cls.score_pos_health1_xy[0] = int(cls.score_pos_health1_xy[0] * cls.font_pos_factor)

            cls.score_pos_level[0] = int(cls.score_pos_level[0] * cls.font_pos_factor)
            cls.score_pos_apples_y = int(cls.score_pos_apples_y * cls.font_pos_factor)
            cls.score_pos_bullets_y = int(cls.score_pos_bullets_y * cls.font_pos_factor)

            cls.score_pos_lives2[0] = int(cls.score_pos_lives2[0] * cls.font_pos_factor)
            cls.score_pos_apples2[0] = int(cls.score_pos_apples2[0] * cls.font_pos_factor)
            cls.score_pos_score2[0] = int(cls.score_pos_score2[0] * cls.font_pos_factor)
            cls.score_pos_health2_xy[0] = int(cls.score_pos_health2_xy[0] * cls.font_pos_factor)
            cls.score_pos_health_size[0] = int(cls.score_pos_health_size[0] * cls.font_pos_factor)
            cls.score_pos_health_size[1] = int(cls.score_pos_health_size[1] * cls.font_pos_factor)
            cls.score_pos_apples_size[0] = int(cls.score_pos_apples_size[0] * cls.font_pos_factor)
            cls.score_pos_apples_size[1] = int(cls.score_pos_apples_size[1] * cls.font_pos_factor)
            cls.score_pos_bullets_size[0] = int(cls.score_pos_bullets_size[0] * cls.font_pos_factor)
            cls.score_pos_bullets_size[1] = int(cls.score_pos_bullets_size[1] * cls.font_pos_factor)

            cls.score_pos_lives1[1] = int(cls.score_pos_lives1[1] * cls.font_pos_factor)
            cls.score_pos_apples1[1] = int(cls.score_pos_apples1[1] * cls.font_pos_factor)
            cls.score_pos_score1[1] = int(cls.score_pos_score1[1] * cls.font_pos_factor)
            cls.score_pos_level[1] = int(cls.score_pos_level[1] * cls.font_pos_factor)
            cls.score_pos_lives2[1] = int(cls.score_pos_lives2[1] * cls.font_pos_factor)
            cls.score_pos_apples2[1] = int(cls.score_pos_apples2[1] * cls.font_pos_factor)
            cls.score_pos_score2[1] = int(cls.score_pos_score2[1] * cls.font_pos_factor)
            cls.score_pos_health1_xy[1] = int(cls.score_pos_health1_xy[1] * cls.font_pos_factor)
            cls.score_pos_health2_xy[1] = int(cls.score_pos_health2_xy[1] * cls.font_pos_factor)
        elif cls.screen_width > 1350:
            cls.font_pos_factor = 1.2

            cls.score_pos_lives1[0] = int(cls.score_pos_lives1[0] * cls.font_pos_factor)
            cls.score_pos_apples1[0] = int(cls.score_pos_apples1[0] * cls.font_pos_factor)
            cls.score_pos_score1[0] = int(cls.score_pos_score1[0] * cls.font_pos_factor)
            cls.score_pos_health1_xy[0] = int(cls.score_pos_health1_xy[0] * cls.font_pos_factor)

            cls.score_pos_level[0] = int(cls.score_pos_level[0] * cls.font_pos_factor)
            cls.score_pos_apples_y = int(cls.score_pos_apples_y * cls.font_pos_factor)
            cls.score_pos_bullets_y = int(cls.score_pos_bullets_y * cls.font_pos_factor)

            cls.score_pos_lives2[0] = int(cls.score_pos_lives2[0] * cls.font_pos_factor)
            cls.score_pos_apples2[0] = int(cls.score_pos_apples2[0] * cls.font_pos_factor)
            cls.score_pos_score2[0] = int(cls.score_pos_score2[0] * cls.font_pos_factor)
            cls.score_pos_health2_xy[0] = int(cls.score_pos_health2_xy[0] * cls.font_pos_factor)

            cls.score_pos_lives1[1] = int(cls.score_pos_lives1[1] * cls.font_pos_factor)
            cls.score_pos_apples1[1] = int(cls.score_pos_apples1[1] * cls.font_pos_factor)
            cls.score_pos_score1[1] = int(cls.score_pos_score1[1] * cls.font_pos_factor)
            cls.score_pos_level[1] = int(cls.score_pos_level[1] * cls.font_pos_factor)
            cls.score_pos_lives2[1] = int(cls.score_pos_lives2[1] * cls.font_pos_factor)
            cls.score_pos_apples2[1] = int(cls.score_pos_apples2[1] * cls.font_pos_factor)
            cls.score_pos_score2[1] = int(cls.score_pos_score2[1] * cls.font_pos_factor)
            cls.score_pos_health1_xy[1] = int(cls.score_pos_health1_xy[1] * cls.font_pos_factor)
            cls.score_pos_health2_xy[1] = int(cls.score_pos_health2_xy[1] * cls.font_pos_factor)

        if cls.screen_height <= SCREEN_MAX_HEIGHT:
            if cls.screen_height < 231:
                cls.screen_near_top = int(cls.screen_height * 0.187)
            elif cls.screen_height < 251:
                cls.screen_near_top = int(cls.screen_height * 0.17)
            elif cls.screen_height < 301:
                cls.screen_near_top = int(cls.screen_height * 0.143)
            elif cls.screen_height < 351:
                cls.screen_near_top = int(cls.screen_height * 0.128)
            elif cls.screen_height < 421:
                cls.screen_near_top = int(cls.screen_height * 0.1)
            elif cls.screen_height < 481:
                cls.screen_near_top = int(cls.screen_height * 0.087)
            elif cls.screen_height < 541:
                cls.screen_near_top = int(cls.screen_height * 0.079)
            elif cls.screen_height < 651:
                cls.screen_near_top = int(cls.screen_height * 0.068)
            elif cls.screen_height < 781:
                cls.screen_near_top = int(cls.screen_height * 0.057)
            elif cls.screen_height < 861:
                cls.screen_near_top = int(cls.screen_height * 0.050)
            elif cls.screen_height < 981:
                cls.screen_near_top = int(cls.screen_height * 0.046)
            else:
                cls.screen_near_top = int(cls.screen_height * 0.04)
        cls.screen_near_top = int(cls.screen_near_top * cls.font_pos_factor * 2)

        # Sprite health bar size and relative position
        cls.score_pos_power_size = cls.score_pos_health_size
        cls.sprite_health_bar_size = lib_jp.Size(w=8 + cls.cell_size * 1.8,
                                                 h=2 + cls.cell_size / 2.5)
        cls.sprite_health_bar_pos_rel = lib_jp.Point(x=-1 + cls.cell_size * 1.2 if cls.cell_size * 1.2 > 8 else 8,
                                                     y=cls.cell_size * 0.8 if cls.cell_size * 0.8 < 9 else 9)
