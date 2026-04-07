import pygame


class BaseState:
    """Base class for all game states."""

    def __init__(self, game):
        self.game = game

    def enter(self):
        """Called when this state becomes active."""
        pass

    def exit(self):
        """Called when this state is removed."""
        pass

    def handle_event(self, event):
        """Handle a single pygame event."""
        pass

    def update(self, dt):
        """Update logic. dt is delta time in seconds."""
        pass

    def draw(self, screen):
        """Draw this state to the screen."""
        pass
