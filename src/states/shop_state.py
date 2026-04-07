import pygame
from src.states.base_state import BaseState
from settings import *


# Weapon definitions for the shop
WEAPONS = {
    "pistol": {"name": "Pistol", "cost": 0, "damage": 10, "fire_rate": 12, "ammo": -1, "desc": "Reliable sidearm. Infinite ammo."},
    "shotgun": {"name": "Shotgun", "cost": 500, "damage": 25, "fire_rate": 30, "ammo": 20, "desc": "Spread shot. Devastating up close."},
    "assault_rifle": {"name": "Assault Rifle", "cost": 800, "damage": 12, "fire_rate": 6, "ammo": 150, "desc": "Full auto. High fire rate."},
    "sniper": {"name": "Sniper Rifle", "cost": 1200, "damage": 80, "fire_rate": 50, "ammo": 10, "desc": "Pierces enemies. Slow but deadly."},
    "flamethrower": {"name": "Flamethrower", "cost": 1500, "damage": 5, "fire_rate": 3, "ammo": 200, "desc": "Short range AoE. Burns over time."},
    "rocket_launcher": {"name": "Rocket Launcher", "cost": 2000, "damage": 100, "fire_rate": 60, "ammo": 5, "desc": "Explosive AoE. Handle with care."},
    "laser_gun": {"name": "Laser Gun", "cost": 3000, "damage": 40, "fire_rate": 8, "ammo": 50, "desc": "Instant hit beam. No travel time."},
}

WEAPON_ORDER = ["pistol", "shotgun", "assault_rifle", "sniper", "flamethrower", "rocket_launcher", "laser_gun"]


class ShopState(BaseState):
    """Weapon shop between levels."""

    def __init__(self, game):
        super().__init__(game)
        self.selected = 0
        self.items = WEAPON_ORDER
        self.title_font = pygame.font.Font(None, 56)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.message = ""
        self.message_timer = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.items)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.items)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._buy_selected()
            elif event.key == pygame.K_ESCAPE:
                self._continue_to_next_level()

    def _buy_selected(self):
        weapon_key = self.items[self.selected]
        weapon = WEAPONS[weapon_key]
        owned = self.game.player_data["weapons"]
        currency = self.game.player_data["currency"]

        if weapon_key in owned:
            self.game.player_data["current_weapon"] = weapon_key
            self.message = f"Equipped {weapon['name']}!"
            self.message_timer = 90
        elif currency >= weapon["cost"]:
            self.game.player_data["currency"] -= weapon["cost"]
            self.game.player_data["weapons"].append(weapon_key)
            self.game.player_data["current_weapon"] = weapon_key
            self.message = f"Purchased {weapon['name']}!"
            self.message_timer = 90
        else:
            self.message = "Not enough $!"
            self.message_timer = 90

    def _continue_to_next_level(self):
        from src.states.play_state import PlayState
        self.game.change_state(PlayState(self.game))

    def update(self, dt):
        if self.message_timer > 0:
            self.message_timer -= 1

    def draw(self, screen):
        screen.fill((15, 12, 20))

        # Title
        title = self.title_font.render("WEAPON SHOP", True, YELLOW)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 50)))

        # Currency
        money = self.font.render(f"$ {self.game.player_data['currency']}", True, YELLOW)
        screen.blit(money, (SCREEN_WIDTH - money.get_width() - 30, 45))

        # Next level hint
        level_text = self.font.render(
            f"Next: Level {self.game.player_data['current_level']}  |  ESC to continue",
            True, GREEN
        )
        screen.blit(level_text, level_text.get_rect(center=(SCREEN_WIDTH // 2, 90)))

        # Weapon list
        owned = self.game.player_data["weapons"]
        equipped = self.game.player_data["current_weapon"]

        for i, weapon_key in enumerate(self.items):
            weapon = WEAPONS[weapon_key]
            y = 130 + i * 70

            # Selection highlight
            if i == self.selected:
                pygame.draw.rect(screen, (40, 35, 55), (60, y - 5, SCREEN_WIDTH - 120, 65), border_radius=5)
                pygame.draw.rect(screen, YELLOW, (60, y - 5, SCREEN_WIDTH - 120, 65), 2, border_radius=5)

            # Status
            if weapon_key in owned:
                if weapon_key == equipped:
                    status = "[EQUIPPED]"
                    status_color = GREEN
                else:
                    status = "[OWNED]"
                    status_color = BLUE
            else:
                status = f"${weapon['cost']}"
                status_color = YELLOW if self.game.player_data["currency"] >= weapon["cost"] else RED

            # Name
            name_color = WHITE if i == self.selected else LIGHT_GRAY
            name = self.font.render(weapon["name"], True, name_color)
            screen.blit(name, (90, y))

            # Stats
            stats_text = f"DMG: {weapon['damage']}  |  Rate: {weapon['fire_rate']}  |  Ammo: {'INF' if weapon['ammo'] == -1 else weapon['ammo']}"
            stats = self.small_font.render(stats_text, True, GRAY)
            screen.blit(stats, (90, y + 28))

            # Description (for selected item)
            if i == self.selected:
                desc = self.small_font.render(weapon["desc"], True, LIGHT_GRAY)
                screen.blit(desc, (90, y + 46))

            # Price/status
            price = self.font.render(status, True, status_color)
            screen.blit(price, (SCREEN_WIDTH - price.get_width() - 90, y + 5))

        # Purchase message
        if self.message_timer > 0:
            msg = self.font.render(self.message, True, GREEN)
            screen.blit(msg, msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)))
