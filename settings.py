# Display
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Dead Zone: Apocalypse"

# Physics
GRAVITY = 0.8
MAX_FALL_SPEED = 15
TILE_SIZE = 32

# Player
PLAYER_SPEED = 5
PLAYER_JUMP_FORCE = -14
PLAYER_MAX_HP = 100
PLAYER_LIVES = 3
PLAYER_INVINCIBILITY_FRAMES = 60  # 1 second at 60fps
PLAYER_ROLL_SPEED = 8
PLAYER_ROLL_DURATION = 20  # frames

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 40, 40)
GREEN = (40, 200, 40)
BLUE = (40, 100, 220)
YELLOW = (240, 220, 40)
DARK_GREEN = (20, 80, 20)
DARK_RED = (120, 20, 20)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
ORANGE = (240, 160, 40)
BROWN = (139, 90, 43)
SKIN_COLOR = (200, 160, 120)
ZOMBIE_SKIN = (120, 160, 100)

# Level
LEVEL_WIDTH_TILES = 200  # tiles wide per level
LEVEL_HEIGHT_TILES = 22  # tiles tall (fits screen height ~704px)
CAMERA_LOOKAHEAD = 100   # pixels to look ahead of player

# Game states
STATE_MENU = "menu"
STATE_PLAY = "play"
STATE_SHOP = "shop"
STATE_PAUSE = "pause"
STATE_GAME_OVER = "game_over"
STATE_VICTORY = "victory"
STATE_LEVEL_COMPLETE = "level_complete"
