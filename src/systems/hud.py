import pygame
from settings import *


class HUD:
    """In-game heads-up display showing health, ammo, currency, wave info."""

    def __init__(self):
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 42)
        self.wave_text = ""
        self.wave_text_timer = 0

    def show_wave_text(self, text, duration=180):
        """Display a large wave announcement."""
        self.wave_text = text
        self.wave_text_timer = duration

    def update(self, dt):
        if self.wave_text_timer > 0:
            self.wave_text_timer -= 1

    def draw(self, screen, player, level, currency):
        """Draw all HUD elements."""
        # Health bar
        bar_x, bar_y = 20, 20
        bar_w, bar_h = 200, 20
        # Background
        pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_w, bar_h))
        # Fill
        fill_w = int(bar_w * (player.hp / player.max_hp))
        if player.hp > player.max_hp * 0.6:
            bar_color = GREEN
        elif player.hp > player.max_hp * 0.3:
            bar_color = YELLOW
        else:
            bar_color = RED
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_w, bar_h))
        # Border
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 2)
        # HP text
        hp_text = self.font.render(f"HP: {player.hp}/{player.max_hp}", True, WHITE)
        screen.blit(hp_text, (bar_x + 5, bar_y + 1))

        # Currency
        coin_text = self.font.render(f"$ {currency}", True, YELLOW)
        screen.blit(coin_text, (20, 50))

        # Level & Wave
        level_text = self.font.render(
            f"Level {level.level_num}  |  Wave {level.current_wave}/{len(level.waves)}",
            True, WHITE
        )
        screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 20, 20))

        # Zombies remaining
        remaining = len(level.zombies) + len(level.zombies_to_spawn)
        if level.wave_active:
            rem_text = self.font.render(f"Zombies: {remaining}", True, ORANGE)
            screen.blit(rem_text, (SCREEN_WIDTH - rem_text.get_width() - 20, 48))

        # Wave announcement
        if self.wave_text_timer > 0:
            alpha = min(255, self.wave_text_timer * 4)
            wave_surf = self.big_font.render(self.wave_text, True, RED)
            wave_surf.set_alpha(alpha)
            rect = wave_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            screen.blit(wave_surf, rect)

        # Controls hint (bottom)
        hint = self.font.render("A/D: Move  |  SPACE: Jump  |  J: Shoot  |  SHIFT: Roll  |  ESC: Pause", True, DARK_GRAY)
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 30))
