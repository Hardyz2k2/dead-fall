import pygame
from settings import *


class Projectile(pygame.sprite.Sprite):
    """A bullet or projectile fired by the player or enemies."""

    def __init__(self, x, y, direction, damage=10, speed=12, color=YELLOW, size=(8, 4), owner="player"):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(float(x), float(y))
        self.direction = direction  # 1 = right, -1 = left
        self.speed = speed
        self.damage = damage
        self.owner = owner
        self.lifetime = 180  # frames before auto-destroy

    def update(self, dt, platforms=None):
        self.pos.x += self.speed * self.direction
        self.rect.centerx = int(self.pos.x)

        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

        # Remove if off-screen (with generous margin)
        if self.rect.right < -100 or self.rect.left > 10000:
            self.kill()

        # Collide with platforms
        if platforms:
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    self.kill()
                    return
