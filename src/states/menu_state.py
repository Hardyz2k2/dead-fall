import pygame
from src.states.base_state import BaseState
from settings import *


class MenuState(BaseState):
    """Main menu with title and options."""

    def __init__(self, game):
        super().__init__(game)
        self.options = ["Start Game", "Quit"]
        self.selected = 0
        self.title_font = pygame.font.Font(None, 80)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.option_font = pygame.font.Font(None, 48)
        self.title_y = 0.0
        self.time = 0.0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._select_option()

    def _select_option(self):
        if self.options[self.selected] == "Start Game":
            from src.states.play_state import PlayState
            self.game.player_data["current_level"] = 1
            self.game.player_data["currency"] = 0
            self.game.player_data["weapons"] = ["pistol"]
            self.game.player_data["upgrades"] = {}
            self.game.player_data["current_weapon"] = "pistol"
            self.game.player_data["lives"] = PLAYER_LIVES
            self.game.change_state(PlayState(self.game))
        elif self.options[self.selected] == "Quit":
            self.game.running = False

    def update(self, dt):
        self.time += dt
        # Gentle float for the title
        import math
        self.title_y = math.sin(self.time * 2) * 8

    def draw(self, screen):
        screen.fill((10, 5, 15))

        # Title
        title_surf = self.title_font.render("DEAD ZONE", True, RED)
        title_rect = title_surf.get_rect(centerx=SCREEN_WIDTH // 2, y=140 + self.title_y)
        screen.blit(title_surf, title_rect)

        # Subtitle
        sub_surf = self.subtitle_font.render("A P O C A L Y P S E", True, DARK_RED)
        sub_rect = sub_surf.get_rect(centerx=SCREEN_WIDTH // 2, y=220 + self.title_y)
        screen.blit(sub_surf, sub_rect)

        # Menu options
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected else GRAY
            text = self.option_font.render(option, True, color)
            rect = text.get_rect(centerx=SCREEN_WIDTH // 2, y=380 + i * 60)
            screen.blit(text, rect)

            if i == self.selected:
                # Draw selector arrow
                arrow = self.option_font.render(">", True, YELLOW)
                screen.blit(arrow, (rect.x - 40, rect.y))

        # Controls hint
        hint = self.subtitle_font.render("W/S to select  |  ENTER to confirm", True, DARK_GRAY)
        hint_rect = hint.get_rect(centerx=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 60)
        screen.blit(hint, hint_rect)
