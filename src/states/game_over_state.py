import pygame
from src.states.base_state import BaseState
from settings import *


class GameOverState(BaseState):
    """Game over or victory screen."""

    def __init__(self, game, victory=False):
        super().__init__(game)
        self.victory = victory
        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 36)
        self.time = 0.0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                from src.states.menu_state import MenuState
                self.game.change_state(MenuState(self.game))

    def update(self, dt):
        self.time += dt

    def draw(self, screen):
        screen.fill((10, 5, 15))

        if self.victory:
            title_text = "YOU SURVIVED!"
            title_color = GREEN
            sub_text = "The apocalypse is over... for now."
        else:
            title_text = "GAME OVER"
            title_color = RED
            sub_text = "The zombies got you."

        # Title
        title = self.title_font.render(title_text, True, title_color)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 250)))

        # Subtitle
        sub = self.font.render(sub_text, True, GRAY)
        screen.blit(sub, sub.get_rect(center=(SCREEN_WIDTH // 2, 330)))

        # Stats
        stats = [
            f"Level Reached: {self.game.player_data['current_level']}",
            f"Currency Earned: ${self.game.player_data['currency']}",
        ]
        for i, stat in enumerate(stats):
            text = self.font.render(stat, True, WHITE)
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, 400 + i * 40)))

        # Prompt
        import math
        alpha = int(128 + 127 * math.sin(self.time * 3))
        prompt = self.font.render("Press ENTER to return to menu", True, YELLOW)
        prompt.set_alpha(alpha)
        screen.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2, 540)))
