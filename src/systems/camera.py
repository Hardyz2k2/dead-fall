import pygame
from settings import *


class Camera:
    """Side-scrolling camera that follows the player."""

    def __init__(self, level_width, level_height):
        self.offset = pygame.math.Vector2(0, 0)
        self.level_width = level_width
        self.level_height = level_height

    def update(self, target):
        """Follow the target (player) with lookahead."""
        # Horizontal: center on player with lookahead
        target_x = target.rect.centerx - SCREEN_WIDTH // 2
        if hasattr(target, 'facing_right'):
            lookahead = CAMERA_LOOKAHEAD if target.facing_right else -CAMERA_LOOKAHEAD
            target_x += lookahead

        # Vertical: center on player
        target_y = target.rect.centery - SCREEN_HEIGHT // 2

        # Smooth follow
        self.offset.x += (target_x - self.offset.x) * 0.1
        self.offset.y += (target_y - self.offset.y) * 0.15

        # Clamp to level boundaries
        self.offset.x = max(0, min(self.offset.x, self.level_width - SCREEN_WIDTH))
        self.offset.y = max(0, min(self.offset.y, self.level_height - SCREEN_HEIGHT))

    def apply(self, rect):
        """Return a rect shifted by the camera offset."""
        return rect.move(-int(self.offset.x), -int(self.offset.y))

    def apply_pos(self, pos):
        """Shift a world position to screen position."""
        return (pos[0] - int(self.offset.x), pos[1] - int(self.offset.y))

    def screen_to_world(self, pos):
        """Convert screen position to world position."""
        return (pos[0] + int(self.offset.x), pos[1] + int(self.offset.y))
