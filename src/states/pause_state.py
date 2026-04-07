import pygame
from src.states.base_state import BaseState
from settings import *


class PauseState(BaseState):
    """Pause overlay on top of gameplay."""

    def __init__(self, game):
        super().__init__(game)
        self.options = ["Resume", "Quit to Menu"]
        self.selected = 0
        self.font = pygame.font.Font(None, 48)
        self.title_font = pygame.font.Font(None, 64)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.pop_state()  # unpause
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._select_option()

    def _select_option(self):
        if self.options[self.selected] == "Resume":
            self.game.pop_state()
        elif self.options[self.selected] == "Quit to Menu":
            from src.states.menu_state import MenuState
            # Clear entire state stack and go to menu
            while self.game.state_stack:
                self.game.pop_state()
            self.game.push_state(MenuState(self.game))

    def draw(self, screen):
        # Draw the gameplay underneath (previous state)
        if len(self.game.state_stack) >= 2:
            self.game.state_stack[-2].draw(screen)

        # Dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # Title
        title = self.title_font.render("PAUSED", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 250)))

        # Options
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected else GRAY
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, 360 + i * 60))
            screen.blit(text, rect)
