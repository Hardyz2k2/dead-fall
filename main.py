#!/usr/bin/env python3
"""Dead Fall - 2D Side-Scrolling Zombie Shooter"""

from src.game import Game
from src.states.menu_state import MenuState


def main():
    game = Game()
    menu = MenuState(game)
    game.push_state(menu)
    game.run()


if __name__ == "__main__":
    main()
