# Samurai Platformer 🎮⚔️

A pixel-art platformer game featuring a relaxing lofi aesthetic, built with Python and Pygame.

## Project Structure

```
Samurai-Platformer/
├── main.py                          # Entry point
├── data/
│   └── assets/
│       ├── fonts/                   # Custom fonts
│       ├── sounds/                  # Audio files
│       └── sprites/                 # Game sprites
│           ├── entities/
│           ├── environment/
│           │   └── biomes/
│           └── ui/
└── scripts/
    ├── config.py                    # Game configuration
    ├── game.py                      # Main game loop
    ├── components/
        └── ui_components/
        └── player_components/
    ├── entities/
    │   └── player.py
    ├── screen_states/
    │   ├── screen_state.py          # Base state class
    └── utilities/
        ├── asset_manager.py         # Asset loading & management
        ├── spritesheet.py           # Spritesheet parser
        └── text.py                  # Text rendering utilities
```

## Controls

*To be implemented with [`PlayerController`](scripts/components/player_controller.py)*

## Technologies

- **Python 3.12.10**
- **Pygame** - Game engine and rendering

## Getting Started
Pygame is currently the only dependency, when more are added i'll make a 'requirements.txt' to install.
```bash
# Install dependencies
pip install pygame

# Run the game
python main.py
```

## Development Notes

- The game uses a state machine pattern for screen management (see [`State`](scripts/screen_states/screen_state.py))
- Assets are loaded centrally through [`AssetManager`](scripts/utilities/asset_manager.py)  

## TODO List
### In Progress

- [ ] **Title Screen Enhancements**
  - [ ] Interactive menu buttons (hover effects, click handling)
  - [ ] Button navigation with keyboard
  - [ ] Animated title text
  - [ ] Buttons actually work

### High Priority

- [ ] **GUI Button Class** (`scripts/utilities/button.py`)
  - [ ] Create reusable Button class with hover/click states
  - [ ] Support for sprite-based buttons
  - [ ] Mouse and keyboard interaction
  - [ ] Callback system for button actions
  - [ ] Integration with [`TitleState`](scripts/screen_states/title_state.py)

- [ ] **Complete Title Screen** ([`TitleState`](scripts/screen_states/title_state.py))
  - [ ] Wire up Play button → start game
  - [ ] Wire up Options button → options menu
  - [ ] Wire up Quit button → exit game
  - [ ] Add button sound effects

### Medium Priority

- [ ] **Game State**
  - [ ] Create PlayState/GameState class
  - [ ] Level loading system

- [ ] **Player Mechanics**
  - [ ] Player movement (walk, run, jump)
  - [ ] Player animations
  - [ ] Collision detection
  - [ ] Gravity and physics

- [ ] **Level Design**
  - [ ] Tilemap system
  - [ ] Level editor or data format
  - [ ] Collectibles and obstacles

### Low Priority

- [ ] **Options Menu**
  - [ ] Volume controls
  - [ ] Key rebinding
  - [ ] Graphics settings

- [ ] **Save/Load System**
  - [ ] Save game progress
  - [ ] Load saved games
  - [ ] Multiple save slots

- [ ] **Polish**
  - [ ] Particle effects
  - [ ] Screen shake
  - [ ] Additional sound effects
  - [ ] More music tracks

  
---
**Author:** Foster Rae  
**Created:** October 23, 2025  
**Status:** In Development