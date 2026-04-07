import pygame
import sys
from settings import *


class Game:
    """Main game class. Manages the game loop and state stack."""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state_stack = []

        # Shared game data persists across states
        self.player_data = {
            "currency": 0,
            "current_level": 1,
            "lives": PLAYER_LIVES,
            "weapons": ["pistol"],
            "upgrades": {},
            "current_weapon": "pistol",
        }

    def push_state(self, state):
        """Push a new state onto the stack."""
        state.enter()
        self.state_stack.append(state)

    def pop_state(self):
        """Pop the top state off the stack."""
        if self.state_stack:
            self.state_stack[-1].exit()
            self.state_stack.pop()

    def change_state(self, state):
        """Replace the top state with a new one."""
        if self.state_stack:
            self.state_stack[-1].exit()
            self.state_stack.pop()
        state.enter()
        self.state_stack.append(state)

    @property
    def current_state(self):
        return self.state_stack[-1] if self.state_stack else None

    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # delta time in seconds

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.current_state:
                    self.current_state.handle_event(event)

            # Update
            if self.current_state:
                self.current_state.update(dt)

            # Draw
            self.screen.fill(BLACK)
            if self.current_state:
                self.current_state.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
