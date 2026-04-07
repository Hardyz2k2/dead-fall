import pygame
from src.states.base_state import BaseState
from src.entities.player import Player
from src.systems.level import Level
from src.systems.camera import Camera
from src.systems.hud import HUD
from src.systems.particles import ParticleSystem
from settings import *


class PlayState(BaseState):
    """Main gameplay state — shooting zombies in a side-scrolling level."""

    def __init__(self, game):
        super().__init__(game)
        self.level_num = game.player_data["current_level"]

    def enter(self):
        # Create level
        self.level = Level(self.level_num)

        # Create player
        spawn = self.level.player_spawn
        self.player = Player(spawn[0], spawn[1])
        self.player_group = pygame.sprite.GroupSingle(self.player)

        # Bullets
        self.player_bullets = pygame.sprite.Group()

        # Camera
        self.camera = Camera(self.level.width, self.level.height)

        # HUD and particles
        self.hud = HUD()
        self.particles = ParticleSystem()

        # Level state
        self.wave_delay = 120  # frames before first wave
        self.between_wave_delay = 0
        self.level_complete = False
        self.death_timer = 0

        # Screen shake
        self.shake_amount = 0
        self.shake_timer = 0

        self.hud.show_wave_text(f"LEVEL {self.level_num}", 180)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from src.states.pause_state import PauseState
                self.game.push_state(PauseState(self.game))
            # Shoot on J or mouse click
            if event.key == pygame.K_j:
                self._player_shoot()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                self._player_shoot()

    def _player_shoot(self):
        if self.player.alive:
            fired = self.player.shoot(self.player_bullets)
            if fired:
                direction = 1 if self.player.facing_right else -1
                bx = self.player.rect.right if self.player.facing_right else self.player.rect.left
                self.particles.emit_muzzle_flash(bx, self.player.rect.centery - 2, direction)

    def _shake_screen(self, amount=5, duration=10):
        self.shake_amount = amount
        self.shake_timer = duration

    def update(self, dt):
        if not self.player.alive:
            self.death_timer += 1
            if self.death_timer > 120:  # 2 seconds after death
                self._handle_death()
            return

        # Player input
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

        # Continuous shooting if holding J or mouse
        if keys[pygame.K_j] or pygame.mouse.get_pressed()[0]:
            self._player_shoot()

        # Update player
        self.player.update(dt, self.level.platforms)

        # Fall death
        if self.player.rect.top > self.level.height + 100:
            self.player.hp = 0

        # Update bullets
        self.player_bullets.update(dt, self.level.platforms)

        # Wave management
        if self.wave_delay > 0:
            self.wave_delay -= 1
            if self.wave_delay == 0:
                self.level.start_next_wave()
                self.hud.show_wave_text(f"WAVE {self.level.current_wave}", 120)
        elif self.between_wave_delay > 0:
            self.between_wave_delay -= 1
            if self.between_wave_delay == 0:
                if not self.level.all_waves_done:
                    self.level.start_next_wave()
                    self.hud.show_wave_text(f"WAVE {self.level.current_wave}", 120)
                else:
                    self._level_complete()
        else:
            self.level.update_spawning(self.camera.offset.x)

            # Check if wave just completed
            if self.level.wave_complete and not self.level.all_waves_done:
                self.between_wave_delay = 120  # 2 second break between waves
                self.level.wave_complete = False
            elif self.level.wave_complete and self.level.all_waves_done:
                self._level_complete()

        # Update zombies
        for zombie in list(self.level.zombies):
            zombie.update(dt, self.level.platforms, self.player)

        # Bullet-zombie collisions
        hits = pygame.sprite.groupcollide(self.player_bullets, self.level.zombies, True, False)
        for bullet, zombies_hit in hits.items():
            for zombie in zombies_hit:
                killed = zombie.take_damage(bullet.damage)
                self.particles.emit_blood(zombie.rect.centerx, zombie.rect.centery, 6)
                if killed:
                    self.game.player_data["currency"] += zombie.currency_reward
                    self.particles.emit_death(zombie.rect.centerx, zombie.rect.centery)
                    zombie.kill()
                    self._shake_screen(3, 6)

        # Zombie-player collisions (contact damage)
        if self.player.alive:
            for zombie in self.level.zombies:
                if self.player.rect.colliderect(zombie.rect):
                    if zombie.can_attack():
                        hit = self.player.take_damage(zombie.damage)
                        if hit:
                            self._shake_screen(6, 12)
                            self.particles.emit_blood(
                                self.player.rect.centerx, self.player.rect.centery, 10
                            )

        # Camera
        self.camera.update(self.player)

        # Particles
        self.particles.update()

        # HUD
        self.hud.update(dt)

        # Shake decay
        if self.shake_timer > 0:
            self.shake_timer -= 1

    def _level_complete(self):
        """All waves cleared — advance to next level."""
        if self.level_complete:
            return
        self.level_complete = True

        if self.level_num >= 10:
            # Game complete!
            from src.states.game_over_state import GameOverState
            self.game.change_state(GameOverState(self.game, victory=True))
        else:
            # Go to shop, then next level
            from src.states.shop_state import ShopState
            self.game.player_data["current_level"] = self.level_num + 1
            self.game.change_state(ShopState(self.game))

    def _handle_death(self):
        """Player died — lose a life or game over."""
        self.game.player_data["lives"] -= 1
        if self.game.player_data["lives"] <= 0:
            from src.states.game_over_state import GameOverState
            self.game.change_state(GameOverState(self.game, victory=False))
        else:
            # Restart this level
            self.game.change_state(PlayState(self.game))

    def draw(self, screen):
        # Shake offset
        import random
        sx, sy = 0, 0
        if self.shake_timer > 0:
            sx = random.randint(-self.shake_amount, self.shake_amount)
            sy = random.randint(-self.shake_amount, self.shake_amount)

        # Background
        self.level.draw_background(screen, self.camera)

        # Platforms
        for platform in self.level.platforms:
            shifted = self.camera.apply(platform.rect).move(sx, sy)
            screen.blit(platform.image, shifted)

        # Zombies
        for zombie in self.level.zombies:
            shifted = self.camera.apply(zombie.rect).move(sx, sy)
            screen.blit(zombie.image, shifted)

        # Player
        if self.player.alive or self.death_timer < 60:
            shifted = self.camera.apply(self.player.rect).move(sx, sy)
            screen.blit(self.player.image, shifted)

        # Bullets
        for bullet in self.player_bullets:
            shifted = self.camera.apply(bullet.rect).move(sx, sy)
            screen.blit(bullet.image, shifted)

        # Particles
        self.particles.draw(screen, self.camera)

        # HUD (not affected by shake)
        self.hud.draw(screen, self.player, self.level, self.game.player_data["currency"])
