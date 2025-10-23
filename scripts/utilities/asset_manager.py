import pygame
import os

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
    data_dir = os.path.join("data")
    assets_dir = os.path.join(data_dir, "assets")
    fonts_dir = os.path.join(assets_dir, 'fonts')
    sprites_dir = os.path.join(assets_dir, "sprites")
    environment_dir = os.path.join(sprites_dir, 'environment')
    biome_dir = os.path.join(environment_dir, 'biome')
    stringstar_fields_dir = os.path.join(environment_dir, 'stringstar_fields')
    
    @staticmethod
    def load_core_assets() -> None:
        """load UI, player and common assets."""
        AssetManager.core_fonts['default'] = pygame.font.Font(os.path.join(AssetManager.fonts_dir,'Virtupetpixies-7O3GV.ttf'), 32)
        AssetManager.core_fonts['Title'] = pygame.font.Font(os.path.join(AssetManager.fonts_dir,'Virtupetpixies-7O3GV.ttf'), 65)
        AssetManager.core_fonts['small'] = pygame.font.Font(os.path.join(AssetManager.fonts_dir,'Virtupetpixies-7O3GV.ttf'), 20)

    @staticmethod
    def load_level_assets(level_name: str) -> None:
        """Load level specific assets.
        Args:
            level_name (str): The name of the level to load the assets for.
        """
        match(level_name):
            case 'starstring_fields':
                AssetManager.level_sprites['bg0'] = pygame.image.load(os.path.join(AssetManager.stringstar_fields_dir, 'background', '0.png'))
                AssetManager.level_sprites['bg1'] = pygame.image.load(os.path.join(AssetManager.stringstar_fields_dir, 'background', '1.png'))
                AssetManager.level_sprites['bg2'] = pygame.image.load(os.path.join(AssetManager.stringstar_fields_dir, 'background', '2.png'))
                
    
    @staticmethod
    def unload_level_assets() -> None:
        """Unload any level specific assets."""
        AssetManager.level_fonts.clear()
        AssetManager.level_sounds.clear()
        AssetManager.level_sprites.clear()