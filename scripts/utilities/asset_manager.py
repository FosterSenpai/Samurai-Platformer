class AssetManager:
    # Core assets to always be loaded
    core_sprites = {}
    core_sounds = {}
    core_fonts = {}
    
    # Level specific assets to be loaded and unloaded per level
    level_sprites = {}
    level_sounds = {}
    level_fonts = {}
    
    @staticmethod
    def load_core_assets() -> None:
        """load UI, player and common assets."""
        pass
    
    @staticmethod
    def load_level_assets(level_name: str) -> None:
        """Load level specific assets.
        Args:
            level_name (str): The name of the level to load the assets for.
        """
        pass
    
    @staticmethod
    def unload_level_assets() -> None:
        """Unload any level specific assets."""
        AssetManager.level_fonts.clear()
        AssetManager.level_sounds.clear()
        AssetManager.level_sprites.clear()