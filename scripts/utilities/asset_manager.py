import pygame
import os
from scripts.config import Config
from scripts.utilities.spritesheet import Spritesheet
from typing import Optional

class AssetManager:
    # Core assets to always be loaded
    player_animations: dict[str, list[pygame.Surface]] = {}
    # TODO: lock the rest of these  vars
    core_sprites = {}
    core_sounds = {}
    core_music: dict[str, str] = {} # track name - file path
    current_track: Optional[str] = None
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
    music_dir = os.path.join(sounds_dir, 'music')
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
        # Sounds
        AssetManager.core_sounds['button_click'] = pygame.mixer.Sound(os.path.join(AssetManager.sounds_dir, 'ui', 'button_click.ogg'))
        AssetManager.core_sounds['notification'] = pygame.mixer.Sound(os.path.join(AssetManager.sounds_dir, 'ui', 'notification.ogg'))
        # Music
        AssetManager.load_all_music_paths()
        
        # Load player animations
        AssetManager.load_player_sprites()
        
    @staticmethod
    def load_player_sprites() -> None:
        """Load all player sprites."""
        anim_dir = os.path.join(AssetManager.sprites_dir, 'entities', 'player')
        idle_sheet = Spritesheet(os.path.join(anim_dir, 'IDLE.png'), frame_count=10, frame_size=(96,96))
        walk_sheet = Spritesheet(os.path.join(anim_dir, 'WALK.png'), frame_count=12, frame_size=(96,96))
        attack_1_sheet = Spritesheet(os.path.join(anim_dir, 'ATTACK 1.png'), frame_count=7, frame_size=(96,96))
        attack_2_sheet = Spritesheet(os.path.join(anim_dir, 'ATTACK 2.png'), frame_count=7, frame_size=(96,96))
        attack_3_sheet = Spritesheet(os.path.join(anim_dir, 'ATTACK 3.png'), frame_count=6, frame_size=(96,96))
        special_attack_sheet = Spritesheet(os.path.join(anim_dir, 'SPECIAL ATTACK.png'), frame_count=14, frame_size=(96,96))
        jump_start_sheet = Spritesheet(os.path.join(anim_dir, 'JUMP-START.png'), frame_count=3, frame_size=(96,96))
        jump_transition_sheet = Spritesheet(os.path.join(anim_dir, 'JUMP-TRANSITION.png'), frame_count=4, frame_size=(96,96))
        jump_fall_sheet = Spritesheet(os.path.join(anim_dir, 'JUMP-FALL.png'), frame_count=2, frame_size=(96,96))
        dash_sheet = Spritesheet(os.path.join(anim_dir, 'DASH.png'), frame_count=8, frame_size=(96,96))
        
        AssetManager.player_animations['idle'] = idle_sheet.parse_frames()
        AssetManager.player_animations['walk'] = walk_sheet.parse_frames()
        AssetManager.player_animations['attack 1'] = attack_1_sheet.parse_frames()
        AssetManager.player_animations['attack 2'] = attack_2_sheet.parse_frames()
        AssetManager.player_animations['attack 3'] = attack_3_sheet.parse_frames()
        AssetManager.player_animations['special attack'] = special_attack_sheet.parse_frames()
        AssetManager.player_animations['jump start'] = jump_start_sheet.parse_frames()
        AssetManager.player_animations['jump transition'] = jump_transition_sheet.parse_frames()
        AssetManager.player_animations['jump fall'] = jump_fall_sheet.parse_frames()
        AssetManager.player_animations['dash'] = dash_sheet.parse_frames()
        
    @staticmethod
    def load_all_music_paths() -> None:
        """Load all music paths into core_sounds dict."""
        for file in os.listdir(AssetManager.music_dir):
            if file.endswith('.ogg'):
                track_name = file.replace('.ogg','')
                AssetManager.core_music[track_name] = os.path.join(AssetManager.music_dir, file)
        
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
        
    @staticmethod
    def unload_core_assets() -> None:
        """Unload core assets."""
        AssetManager.core_fonts.clear()
        AssetManager.core_sounds.clear()
        AssetManager.core_sprites.clear()
        AssetManager.core_music.clear()
        AssetManager.player_animations.clear()
        
    # MUSIC CONTROLS
    @staticmethod
    def play_music(track_name: str, volume: float = 0.5, loops: int = -1) -> None:
        """Play music track by name.
        Args:
            track_name (str): The name of the track to play.
            loops (int): Number of loops (-1 for infinite).
            volume (float): Volume level (0.0 to 1.0).
        """
        if track_name in AssetManager.core_music:
            AssetManager.current_track = track_name
            pygame.mixer.music.load(AssetManager.core_music[track_name])
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops)
        else:
            print(f"Music track '{track_name}' not found!")
            
    @staticmethod
    def fade_music(duration_ms: int) -> None:
        """Fade out current music over duration.
        Args:
            duration_ms (int): Duration in milliseconds to fade out.
        """
        pygame.mixer.music.fadeout(duration_ms)
        AssetManager.current_track = None
        
    @staticmethod
    def stop_music() -> None:
        """Stop current music immediately."""
        pygame.mixer.music.stop()
        AssetManager.current_track = None