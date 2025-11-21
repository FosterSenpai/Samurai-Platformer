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
When more are added i'll make a 'requirements.txt' to install.
```bash
# Install dependencies
pip install pygame
pip install pydub

# Run the game
python main.py
```

## Development Notes

- The game uses a state machine pattern for screen management (see [`State`](scripts/screen_states/screen_state.py))
- Assets are loaded centrally through [`AssetManager`](scripts/utilities/asset_manager.py)  

## TODO List
### In Progress
2- [ ] **Load & Options States**
  - [ ] Draw over title state as popups.

- [ ] **Enemy samurai class**
  - [ ] need enemy class
  - [ ] Decide how per level loading is going to work, load all enemies per level in own func?
  - [ ] Add sounds, maybe same as player just pydub the pitch

- [ ] **Large Level Asset Cache**
  - [ ] to speed up transitions back to a level just left, implement a small cache to store large assets to try avoid loading again.

- [ ] **Level Loading**
  - [ ] Move test scenario into a loadable level.

- [ ] **Testing UI**
  - [ ] Add UI for button inputs, change ui based on what current input device is, xbox kbm, ps etc. Maybe a dict mapping the config input to the incon and drawing the icon based on input device, there will be a clean way to do it.

### Future Ideas
- Definitely need a controllable music player.
  
---
**Author:** Foster Rae  
**Created:** October 23, 2025  
**Status:** In Development