import pygame
import random
from settings import *


class Zombie(pygame.sprite.Sprite):
    """Base zombie class. All zombie types extend this."""

    def __init__(self, x, y, zombie_type="walker", level=1):
        super().__init__()
        self.zombie_type = zombie_type
        self.level = level

        # Get stats for this type
        stats = ZOMBIE_STATS.get(zombie_type, ZOMBIE_STATS["walker"])
        level_scale = 1 + 0.15 * (level - 1)

        self.max_hp = int(stats["hp"] * level_scale)
        self.hp = self.max_hp
        self.speed = stats["speed"] * (1 + 0.05 * (level - 1))
        self.damage = int(stats["damage"] * level_scale)
        self.attack_cooldown = 0
        self.attack_rate = stats.get("attack_rate", 60)
        self.currency_reward = stats.get("currency", 10)
        self.color = stats["color"]
        self.shirt_color = stats.get("shirt_color", (100, 100, 100))

        # Physics
        self.width = 28
        self.height = 44
        self.image = self._create_sprite()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = pygame.math.Vector2(float(x), float(y))
        self.vel = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.facing_right = False  # zombies usually face left (toward player)

        # AI
        self.state = "walk"
        self.hit_flash = 0

    def _create_sprite(self):
        """Create a zombie sprite with ripped clothing."""
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Body / torso with ripped t-shirt
        shirt = self.shirt_color
        pygame.draw.rect(surf, shirt, (4, 14, 20, 16))
        # Ripped edges on shirt (irregular bottom)
        for i in range(4, 24, 3):
            tear_h = random.randint(0, 4)
            pygame.draw.rect(surf, (0, 0, 0, 0), (i, 30 - tear_h, 2, tear_h + 2))
        # Shirt tears / holes
        if random.random() > 0.5:
            pygame.draw.rect(surf, self.color, (8, 18, 4, 3))  # skin showing through tear
        if random.random() > 0.5:
            pygame.draw.rect(surf, self.color, (16, 20, 5, 2))

        # Head (zombie skin)
        pygame.draw.rect(surf, self.color, (7, 2, 14, 12))
        # Zombie eyes (red/glowing)
        pygame.draw.rect(surf, RED, (10, 6, 3, 3))
        pygame.draw.rect(surf, RED, (17, 6, 3, 3))
        # Mouth
        pygame.draw.rect(surf, DARK_RED, (11, 10, 6, 2))

        # Arms (zombie skin)
        pygame.draw.rect(surf, self.color, (0, 16, 4, 10))
        pygame.draw.rect(surf, self.color, (24, 16, 4, 10))

        # Legs with ripped pants
        pants_color = (60, 50, 40)  # dark brown ripped pants
        pygame.draw.rect(surf, pants_color, (6, 30, 7, 10))
        pygame.draw.rect(surf, pants_color, (15, 30, 7, 10))
        # Ripped pant legs
        for i in range(6, 22, 4):
            if random.random() > 0.4:
                tear_h = random.randint(1, 3)
                pygame.draw.rect(surf, self.color, (i, 38 - tear_h, 3, tear_h))

        # Feet
        pygame.draw.rect(surf, (40, 35, 30), (5, 40, 8, 4))
        pygame.draw.rect(surf, (40, 35, 30), (15, 40, 8, 4))

        return surf

    def take_damage(self, amount):
        """Take damage, return True if killed."""
        self.hp -= amount
        self.hit_flash = 6
        if self.hp <= 0:
            self.hp = 0
            return True
        return False

    def update(self, dt, platforms, player):
        """Update zombie AI and physics."""
        if self.hit_flash > 0:
            self.hit_flash -= 1

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Simple AI: walk toward player
        if player and player.alive:
            if player.rect.centerx < self.rect.centerx:
                self.vel.x = -self.speed
                self.facing_right = False
            else:
                self.vel.x = self.speed
                self.facing_right = True
        else:
            self.vel.x = 0

        # Gravity
        self.vel.y += GRAVITY
        if self.vel.y > MAX_FALL_SPEED:
            self.vel.y = MAX_FALL_SPEED

        # Move X
        self.pos.x += self.vel.x
        self.rect.x = int(self.pos.x)
        self._collide_x(platforms)

        # Move Y
        self.pos.y += self.vel.y
        self.rect.y = int(self.pos.y)
        self._collide_y(platforms)

        # Update sprite direction
        base = self._create_sprite()
        if self.facing_right:
            self.image = pygame.transform.flip(base, True, False)
        else:
            self.image = base

        # Hit flash (white overlay)
        if self.hit_flash > 0:
            flash_surf = self.image.copy()
            flash_surf.fill((255, 255, 255, 120), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = flash_surf

    def can_attack(self):
        """Check if zombie can deal contact damage."""
        if self.attack_cooldown > 0:
            return False
        self.attack_cooldown = self.attack_rate
        return True

    def _collide_x(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel.x > 0:
                    self.rect.right = platform.rect.left
                elif self.vel.x < 0:
                    self.rect.left = platform.rect.right
                self.pos.x = float(self.rect.x)

    def _collide_y(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel.y > 0:
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.vel.y = 0
                elif self.vel.y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel.y = 0
                self.pos.y = float(self.rect.y)


# Zombie type stats
ZOMBIE_STATS = {
    "walker": {
        "hp": 30,
        "speed": 1.0,
        "damage": 10,
        "attack_rate": 60,
        "currency": 10,
        "color": ZOMBIE_SKIN,
        "shirt_color": (120, 60, 60),  # reddish torn shirt
    },
    "runner": {
        "hp": 25,
        "speed": 2.5,
        "damage": 8,
        "attack_rate": 45,
        "currency": 15,
        "color": (100, 140, 90),
        "shirt_color": (80, 80, 120),  # blue-ish torn shirt
    },
    "spitter": {
        "hp": 20,
        "speed": 1.2,
        "damage": 12,
        "attack_rate": 90,
        "currency": 20,
        "color": (80, 150, 60),
        "shirt_color": (100, 100, 50),  # yellowish shirt
    },
    "brute": {
        "hp": 80,
        "speed": 0.7,
        "damage": 20,
        "attack_rate": 80,
        "currency": 30,
        "color": (90, 120, 80),
        "shirt_color": (70, 70, 70),  # dark gray shirt
    },
    "crawler": {
        "hp": 15,
        "speed": 1.5,
        "damage": 8,
        "attack_rate": 40,
        "currency": 15,
        "color": (110, 140, 100),
        "shirt_color": (90, 60, 50),  # brown shirt
    },
    "exploder": {
        "hp": 20,
        "speed": 2.0,
        "damage": 25,
        "attack_rate": 999,  # explodes once
        "currency": 25,
        "color": (160, 120, 80),
        "shirt_color": (140, 50, 50),  # red shirt
    },
    "screamer": {
        "hp": 35,
        "speed": 0.8,
        "damage": 5,
        "attack_rate": 120,
        "currency": 30,
        "color": (140, 160, 130),
        "shirt_color": (110, 110, 130),  # purple-gray shirt
    },
    "jumper": {
        "hp": 30,
        "speed": 2.0,
        "damage": 15,
        "attack_rate": 50,
        "currency": 20,
        "color": (100, 130, 90),
        "shirt_color": (60, 90, 60),  # green shirt
    },
}
