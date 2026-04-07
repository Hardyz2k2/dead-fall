import pygame
import random
from settings import *
from src.entities.zombie import Zombie


class Platform(pygame.sprite.Sprite):
    """A solid platform/tile the player can stand on."""

    def __init__(self, x, y, width, height, color=None):
        super().__init__()
        self.image = pygame.Surface((width, height))
        if color is None:
            color = (60, 55, 50)
        self.image.fill(color)
        # Top edge highlight
        if height >= TILE_SIZE:
            pygame.draw.rect(self.image, (80, 120, 50), (0, 0, width, 3))
        self.rect = self.image.get_rect(topleft=(x, y))


class Level:
    """Manages level layout, waves, and spawning."""

    def __init__(self, level_num):
        self.level_num = level_num
        self.platforms = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()

        # Level dimensions
        self.width = LEVEL_WIDTH_TILES * TILE_SIZE
        self.height = LEVEL_HEIGHT_TILES * TILE_SIZE

        # Wave system
        self.waves = self._define_waves()
        self.current_wave = 0
        self.wave_active = False
        self.zombies_to_spawn = []
        self.spawn_timer = 0
        self.spawn_interval = 60  # frames between spawns
        self.wave_complete = False
        self.all_waves_done = False
        self.boss_spawned = False

        # Parallax backgrounds
        self.bg_layers = self._create_backgrounds()

        # Build the level
        self._build_level()

    def _create_backgrounds(self):
        """Create parallax background layers."""
        layers = []

        # Far background (sky)
        sky = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        sky_colors = [
            (15, 10, 25),   # dark purple night sky
            (25, 15, 35),
            (20, 12, 30),
        ]
        sky.fill(sky_colors[self.level_num % len(sky_colors)])
        # Stars
        for _ in range(80):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT // 2)
            size = random.randint(1, 2)
            brightness = random.randint(100, 255)
            pygame.draw.rect(sky, (brightness, brightness, brightness), (x, y, size, size))
        layers.append({"surface": sky, "speed": 0.05})

        # Mid background (buildings/silhouettes)
        mid = pygame.Surface((SCREEN_WIDTH * 2, SCREEN_HEIGHT), pygame.SRCALPHA)
        building_color = (20, 18, 25)
        for i in range(15):
            bw = random.randint(60, 150)
            bh = random.randint(100, 350)
            bx = i * 180 + random.randint(-30, 30)
            by = SCREEN_HEIGHT - bh
            pygame.draw.rect(mid, building_color, (bx, by, bw, bh))
            # Windows (some lit)
            for wy in range(by + 10, by + bh - 20, 25):
                for wx in range(bx + 8, bx + bw - 15, 20):
                    if random.random() > 0.7:
                        pygame.draw.rect(mid, (180, 160, 60), (wx, wy, 8, 10))
                    else:
                        pygame.draw.rect(mid, (30, 28, 35), (wx, wy, 8, 10))
        layers.append({"surface": mid, "speed": 0.3})

        return layers

    def _build_level(self):
        """Build platforms for this level."""
        ground_y = self.height - TILE_SIZE * 2

        # Ground (full level width)
        for x in range(0, self.width, TILE_SIZE):
            self.platforms.add(Platform(x, ground_y, TILE_SIZE, TILE_SIZE * 2, (50, 45, 40)))

        # Floating platforms spread throughout
        platform_configs = self._get_platform_layout()
        for px, py, pw in platform_configs:
            self.platforms.add(Platform(px, py, pw, TILE_SIZE, (70, 65, 55)))

    def _get_platform_layout(self):
        """Generate platform positions based on level number."""
        platforms = []
        ground_y = self.height - TILE_SIZE * 2
        random.seed(self.level_num * 42)  # deterministic per level

        # Scattered platforms throughout the level
        for i in range(20 + self.level_num * 3):
            x = 300 + i * random.randint(150, 350)
            if x > self.width - 200:
                break
            y = ground_y - random.randint(80, 220)
            w = random.choice([TILE_SIZE * 3, TILE_SIZE * 4, TILE_SIZE * 5])
            platforms.append((x, y, w))

        # Some higher platforms
        for i in range(5 + self.level_num):
            x = 500 + i * random.randint(300, 500)
            if x > self.width - 200:
                break
            y = ground_y - random.randint(200, 340)
            w = random.choice([TILE_SIZE * 2, TILE_SIZE * 3])
            platforms.append((x, y, w))

        return platforms

    def _define_waves(self):
        """Define zombie waves for this level."""
        waves = []
        # Available zombie types per level
        available_types = {
            1: ["walker"],
            2: ["walker", "runner"],
            3: ["walker", "runner", "spitter"],
            4: ["walker", "runner", "spitter", "brute"],
            5: ["walker", "runner", "spitter", "brute", "crawler"],
            6: ["walker", "runner", "spitter", "brute", "crawler", "exploder"],
            7: ["walker", "runner", "spitter", "brute", "crawler", "exploder", "screamer"],
            8: ["walker", "runner", "spitter", "brute", "crawler", "exploder", "screamer", "jumper"],
            9: ["walker", "runner", "spitter", "brute", "crawler", "exploder", "screamer", "jumper"],
            10: ["walker", "runner", "spitter", "brute", "crawler", "exploder", "screamer", "jumper"],
        }

        types = available_types.get(self.level_num, available_types[10])
        num_waves = 3 + (self.level_num // 3)  # 3-6 waves

        for wave_num in range(num_waves):
            wave = []
            count = 3 + self.level_num + wave_num * 2
            for _ in range(count):
                # Weight newer zombie types higher in later waves
                zombie_type = random.choice(types)
                wave.append(zombie_type)
            waves.append(wave)

        return waves

    def start_next_wave(self):
        """Begin spawning the next wave of zombies."""
        if self.current_wave >= len(self.waves):
            self.all_waves_done = True
            return False

        self.zombies_to_spawn = list(self.waves[self.current_wave])
        self.wave_active = True
        self.wave_complete = False
        self.spawn_timer = 0
        self.current_wave += 1
        return True

    def update_spawning(self, camera_offset_x):
        """Spawn zombies from the current wave."""
        if not self.wave_active:
            return

        self.spawn_timer -= 1
        if self.spawn_timer <= 0 and self.zombies_to_spawn:
            zombie_type = self.zombies_to_spawn.pop(0)
            self.spawn_timer = self.spawn_interval

            # Spawn off-screen to the right (or left sometimes)
            ground_y = self.height - TILE_SIZE * 2 - 44  # zombie height
            side = random.choice(["right", "right", "left"])  # mostly from right
            if side == "right":
                spawn_x = camera_offset_x + SCREEN_WIDTH + random.randint(50, 200)
            else:
                spawn_x = camera_offset_x - random.randint(50, 200)

            zombie = Zombie(spawn_x, ground_y, zombie_type, self.level_num)
            self.zombies.add(zombie)

        # Check if wave is complete (all spawned and all dead)
        if not self.zombies_to_spawn and len(self.zombies) == 0:
            self.wave_active = False
            self.wave_complete = True

    def draw_background(self, screen, camera):
        """Draw parallax backgrounds."""
        for layer in self.bg_layers:
            offset_x = int(camera.offset.x * layer["speed"])
            surf = layer["surface"]
            # Tile the background horizontally
            sw = surf.get_width()
            start_x = -(offset_x % sw)
            for x in range(int(start_x), SCREEN_WIDTH + sw, sw):
                screen.blit(surf, (x, 0))

    @property
    def player_spawn(self):
        """Where the player starts in this level."""
        ground_y = self.height - TILE_SIZE * 2 - 48  # above ground
        return (100, ground_y)
