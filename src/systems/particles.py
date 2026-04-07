import pygame
import random
from settings import *


class Particle:
    """A single visual particle."""

    def __init__(self, x, y, color, vel_x=0, vel_y=0, lifetime=30, size=3):
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.alive = True

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.15  # gravity
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.alive = False

    def draw(self, screen, camera):
        if not self.alive:
            return
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        sx, sy = camera.apply_pos((self.x, self.y))
        size = max(1, int(self.size * (self.lifetime / self.max_lifetime)))
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        surf.fill((*self.color[:3], alpha))
        screen.blit(surf, (sx, sy))


class ParticleSystem:
    """Manages all active particles."""

    def __init__(self):
        self.particles = []

    def emit_blood(self, x, y, count=8):
        """Spawn blood particles at position."""
        for _ in range(count):
            vx = random.uniform(-3, 3)
            vy = random.uniform(-4, 0)
            color = random.choice([RED, DARK_RED, (180, 30, 30)])
            size = random.randint(2, 4)
            life = random.randint(15, 35)
            self.particles.append(Particle(x, y, color, vx, vy, life, size))

    def emit_muzzle_flash(self, x, y, direction):
        """Spawn muzzle flash particles."""
        for _ in range(5):
            vx = direction * random.uniform(2, 6)
            vy = random.uniform(-1, 1)
            color = random.choice([YELLOW, ORANGE, WHITE])
            self.particles.append(Particle(x, y, color, vx, vy, 8, random.randint(2, 4)))

    def emit_death(self, x, y, color=RED, count=15):
        """Spawn death explosion particles."""
        for _ in range(count):
            vx = random.uniform(-4, 4)
            vy = random.uniform(-5, 1)
            size = random.randint(2, 5)
            life = random.randint(20, 45)
            self.particles.append(Particle(x, y, color, vx, vy, life, size))

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.alive]

    def draw(self, screen, camera):
        for p in self.particles:
            p.draw(screen, camera)
