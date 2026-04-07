import pygame
from settings import *
from src.entities.projectile import Projectile


class Player(pygame.sprite.Sprite):
    """The player character — side-scroller hero."""

    def __init__(self, x, y):
        super().__init__()
        # Visual
        self.width = 28
        self.height = 44
        self.image = self._create_sprite()
        self.rect = self.image.get_rect(topleft=(x, y))

        # Physics
        self.pos = pygame.math.Vector2(float(x), float(y))
        self.vel = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.facing_right = True

        # Combat
        self.hp = PLAYER_MAX_HP
        self.max_hp = PLAYER_MAX_HP
        self.invincible_timer = 0
        self.shoot_cooldown = 0
        self.shoot_rate = 12  # frames between shots

        # Roll
        self.rolling = False
        self.roll_timer = 0

    def _create_sprite(self):
        """Create a simple placeholder player sprite."""
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Body (dark green jacket)
        pygame.draw.rect(surf, (50, 80, 50), (4, 14, 20, 18))
        # Head
        pygame.draw.rect(surf, SKIN_COLOR, (7, 2, 14, 12))
        # Hair
        pygame.draw.rect(surf, BROWN, (7, 2, 14, 4))
        # Eyes
        pygame.draw.rect(surf, BLACK, (10, 7, 3, 2))
        pygame.draw.rect(surf, BLACK, (17, 7, 3, 2))
        # Legs (dark pants)
        pygame.draw.rect(surf, (40, 40, 60), (6, 32, 7, 12))
        pygame.draw.rect(surf, (40, 40, 60), (15, 32, 7, 12))
        # Boots
        pygame.draw.rect(surf, (30, 30, 30), (5, 40, 8, 4))
        pygame.draw.rect(surf, (30, 30, 30), (15, 40, 8, 4))

        return surf

    def handle_input(self, keys):
        """Process keyboard input for movement."""
        if self.rolling:
            return

        # Horizontal movement
        self.vel.x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel.x = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel.x = PLAYER_SPEED
            self.facing_right = True

        # Jump
        if (keys[pygame.K_w] or keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel.y = PLAYER_JUMP_FORCE
            self.on_ground = False

        # Roll
        if keys[pygame.K_LSHIFT] and self.on_ground and not self.rolling:
            self.rolling = True
            self.roll_timer = PLAYER_ROLL_DURATION
            self.vel.x = PLAYER_ROLL_SPEED * (1 if self.facing_right else -1)

    def shoot(self, bullet_group):
        """Fire a bullet in the facing direction. Returns True if fired."""
        if self.shoot_cooldown > 0:
            return False
        self.shoot_cooldown = self.shoot_rate

        direction = 1 if self.facing_right else -1
        bx = self.rect.right if self.facing_right else self.rect.left
        by = self.rect.centery - 2
        bullet = Projectile(bx, by, direction, damage=10, speed=12, color=YELLOW)
        bullet_group.add(bullet)
        return True

    def take_damage(self, amount):
        """Take damage if not invincible. Returns True if damage applied."""
        if self.invincible_timer > 0 or self.rolling:
            return False
        self.hp -= amount
        self.invincible_timer = PLAYER_INVINCIBILITY_FRAMES
        if self.hp <= 0:
            self.hp = 0
        return True

    def update(self, dt, platforms):
        """Update physics, handle collisions with platforms."""
        # Timers
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        # Roll
        if self.rolling:
            self.roll_timer -= 1
            if self.roll_timer <= 0:
                self.rolling = False

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

        # Clamp to level (don't go left of 0)
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = float(self.rect.x)

        # Update sprite flip
        if not self.facing_right:
            self.image = pygame.transform.flip(self._create_sprite(), True, False)
        else:
            self.image = self._create_sprite()

        # Invincibility flash
        if self.invincible_timer > 0 and self.invincible_timer % 6 < 3:
            self.image.set_alpha(100)
        else:
            self.image.set_alpha(255)

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

    @property
    def alive(self):
        return self.hp > 0
