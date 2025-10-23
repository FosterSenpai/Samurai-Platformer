import pygame
import os
from scripts.config import Config
from scripts.utilities.spritesheet import Spritesheet

class AssetManager:
    # Core assets to always be loaded
    core_sprites = {}
    core_sounds = {}
    core_fonts = {}
    
    # Level specific assets to be loaded and unloaded per level
    level_sprites = {}
    level_sounds = {}
    level_fonts = {}
    
    # Pointers to directories
    data_dir = os.path.join('data')
    assets_dir = os.path.join(data_dir, 'assets')
    fonts_dir = os.path.join(assets_dir, 'fonts')
    sounds_dir = os.path.join(assets_dir, 'sounds')
    sprites_dir = os.path.join(assets_dir, 'sprites')
    ui_sprites_dir = os.path.join(sprites_dir, 'ui')
    environment_sprites_dir = os.path.join(sprites_dir, 'environment')
    biome_sprites_dir = os.path.join(environment_sprites_dir, 'biomes')
    stringstar_fields_sprites_dir = os.path.join(biome_sprites_dir, 'stringstar_fields')
    
    @staticmethod
    def load_core_assets() -> None:
        """load UI, player and common assets."""
        # Fonts
        AssetManager.core_fonts['default'] = pygame.font.Font(os.path.join(AssetManager.fonts_dir,'Virtupetpixies-7O3GV.ttf'), 32)
        AssetManager.core_fonts['title'] = pygame.font.Font(os.path.join(AssetManager.fonts_dir,'Virtupetpixies-7O3GV.ttf'), 65)
        AssetManager.core_fonts['small'] = pygame.font.Font(os.path.join(AssetManager.fonts_dir,'Virtupetpixies-7O3GV.ttf'), 20)
        # Load UI
        ui_sheet = Spritesheet(os.path.join(AssetManager.ui_sprites_dir, 'humble_UI_sheet.png'))
        ui_sprites = ui_sheet.parse_spritesheet()
        for name, sprite in ui_sprites.items():
            AssetManager.core_sprites[f'ui_{name}'] = sprite
        # Menu Backgrounds (using stringstar fields bg for now)
        AssetManager.core_sprites['bg0'] = pygame.image.load(os.path.join(AssetManager.stringstar_fields_sprites_dir, 'background', '0.png'))
        AssetManager.core_sprites['bg1'] = pygame.image.load(os.path.join(AssetManager.stringstar_fields_sprites_dir, 'background', '1.png'))
        AssetManager.core_sprites['bg2'] = pygame.image.load(os.path.join(AssetManager.stringstar_fields_sprites_dir, 'background', '2.png'))
        # Rescaling sprites
        for sprite_name, sprite_surface in AssetManager.core_sprites.items():
            # Rescaling bg to game size
            if 'bg' in sprite_name:
                AssetManager.core_sprites[sprite_name] = pygame.transform.scale(sprite_surface, (Config.GAME_W * 2, Config.GAME_H))
        # Audio
        pygame.mixer.init()
        # Storing paths for music, music is loaded per screen/state
        AssetManager.core_sounds['evening mood'] = os.path.join(AssetManager.sounds_dir, 'evening mood.ogg')
    
    @staticmethod
    def load_level_assets(level_name: str) -> None:
        """Load level specific assets.
        Args:
            level_name (str): The name of the level to load the assets for.
        """
        match(level_name):
            case 'starstring_fields':
                AssetManager.level_sprites['bg0'] = pygame.image.load(os.path.join(AssetManager.stringstar_fields_sprites_dir, 'background', '0.png'))
                AssetManager.level_sprites['bg1'] = pygame.image.load(os.path.join(AssetManager.stringstar_fields_sprites_dir, 'background', '1.png'))
                AssetManager.level_sprites['bg2'] = pygame.image.load(os.path.join(AssetManager.stringstar_fields_sprites_dir, 'background', '2.png'))
                
    
    @staticmethod
    def unload_level_assets() -> None:
        """Unload any level specific assets."""
        AssetManager.level_fonts.clear()
        AssetManager.level_sounds.clear()
        AssetManager.level_sprites.clear()