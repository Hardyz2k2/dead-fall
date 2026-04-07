# Dead Fall — 2D Side-Scrolling Zombie Shooter

## Project Overview
A 2D side-scrolling zombie shooter (Metal Slug / Contra style) built with **Python + Pygame**, targeting Steam release.

- **Genre**: Side-scroller shooter
- **Theme**: Zombie apocalypse
- **Levels**: 10, each ending with a unique boss fight
- **Progression**: New zombie types introduced each level, all enemies scale in difficulty
- **Economy**: Currency from kills → weapon shop between levels
- **Art**: Programmatic pixel art (zombies wear ripped t-shirts and pants)

## Tech Stack
- Python 3.13 + Pygame 2.6
- Packaged for Steam via PyInstaller
- Repo: https://github.com/Hardyz2k2/dead-fall

## Architecture
- **Stack-based state machine**: MenuState → PlayState → ShopState → next level (push/pop for pause overlay)
- **Pygame sprite groups** for collision: players, zombies, player_bullets, platforms
- **Delta-time game loop** at 60 FPS
- **Side-scrolling camera** with smooth follow + directional look-ahead

## Project Structure
```
main.py              → Entry point
settings.py          → All constants (screen, physics, colors, keys)
src/game.py          → Game class (loop, state stack, shared player_data)
src/states/          → State machine states (menu, play, shop, pause, game_over)
src/entities/        → Player, Zombie, Projectile, Boss
src/systems/         → Camera, Level, HUD, Particles, Weapon, Shop, Audio, SaveManager
src/utils/           → SpriteSheet loader, PixelArtGenerator
assets/              → sprites/, tiles/, sounds/, music/, fonts/
data/                → weapons.json, zombies.json, bosses.json, levels.json, shop.json
```

## Key Design Decisions
- Zombie stats scale per level: `base_stat * (1 + 0.15 * (level - 1))`
- All zombie/weapon/boss stats live in JSON data files for easy balance tuning
- SteamManager wraps all Steam calls in try/except — game runs fine without Steam
- Sprites are generated programmatically (PixelArtGenerator) and cached — replaceable with real art later

## Zombie Types (introduced per level)
1. Walker (slow, melee) → 2. Runner (fast) → 3. Spitter (ranged) → 4. Brute (tanky) → 5. Crawler (low) → 6. Exploder (AoE death) → 7. Screamer (buffs allies) → 8. Jumper (aerial) → 9. Elite variants (2x stats) → 10. All + final boss

## Bosses
L1: Mega Walker | L2: Horde Master | L3: Acid Queen | L4: The Tank | L5: Tunnel Worm | L6: The Detonator | L7: Banshee | L8: Sky Stalker | L9: The Amalgamation | L10: Patient Zero (3-phase)

## Weapons (shop)
Pistol (free) → Shotgun ($500) → Assault Rifle ($800) → Sniper ($1200) → Flamethrower ($1500) → Rocket Launcher ($2000) → Laser Gun ($3000). Each has 3-tier upgrades (damage, fire rate, ammo, reload).

## Controls
A/D or Arrows: Move | Space/W: Jump | J or Left Click: Shoot | Shift: Roll | Q/E: Switch weapon | ESC: Pause

## Current Progress
- **Phase 1 COMPLETE** ✅ — Playable prototype with player, walkers, shooting, camera, HUD, shop, pause, game over
- **Phase 2**: TODO — All zombie type behaviors, weapon system with ammo/switching, full particle effects
- **Phase 3**: TODO — All 10 bosses, level themes, level loading from JSON
- **Phase 4**: TODO — Weapon upgrades in shop, save/load system, balance tuning
- **Phase 5**: TODO — Pixel art polish, audio/SFX/music, menu settings
- **Phase 6**: TODO — Steam integration, achievements, PyInstaller packaging

## How to Run
```bash
pip install pygame
python3 main.py
```
