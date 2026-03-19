import pygame
import os
from scripts.config import Config
from scripts.utilities.spritesheet import Spritesheet
from typing import Optional
# Suppress pydub warning, its doing what it needs to do fine
import warnings
warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv", category=RuntimeWarning, module="pydub.utils")
from pydub import AudioSegment
from pydub.playback import play
import io

class AssetManager:
    # Core assets to always be loaded
    # TODO: lock the rest of these  vars
    core_sprites = {}
    core_sounds = {}
    core_music: dict[str, str] = {} # track name - file path
    current_track: Optional[str] = None
    core_fonts = {}
    
    # Player assets
    player_animations: dict[str, list[pygame.Surface]] = {}
    player_sounds: dict[str, pygame.mixer.Sound] = {}
    
    # Level specific assets to be loaded and unloaded per level
    level_enemies_animations: dict[str, dict[str, pygame.Surface]] = {} # enemy -> dict of animations, animation name -> frames
    level_enemies_sounds: dict[str, dict[str, pygame.mixer.Sound]] = {} # enemy -> dict of sounds, sound name -> sound
    level_sprites = {}
    level_sounds = {}
    level_fonts = {}
    
    # Pointers to directories
    data_dir: str = os.path.join('data')
    assets_dir: str = os.path.join(data_dir, 'assets')
    fonts_dir: str = os.path.join(assets_dir, 'fonts')
    sounds_dir: str = os.path.join(assets_dir, 'sounds')
    music_dir: str = os.path.join(sounds_dir, 'music')
    sprites_dir: str = os.path.join(assets_dir, 'sprites')
    ui_sprites_dir: str = os.path.join(sprites_dir, 'ui')
    environment_sprites_dir: str = os.path.join(sprites_dir, 'environment')
    biome_sprites_dir: str = os.path.join(environment_sprites_dir, 'biomes')
    stringstar_fields_sprites_dir: str = os.path.join(biome_sprites_dir, 'stringstar_fields')
    
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
        # Menu Backgrounds
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
        
        AssetManager.load_player_assets()
        
    @staticmethod
    def load_player_assets() -> None:
        """Load all player assets."""
        AssetManager.load_animations_folder(os.path.join(AssetManager.sprites_dir, 'entities', 'player'), AssetManager.player_animations)
        AssetManager.load_sounds_folder(os.path.join(AssetManager.sounds_dir, 'fx', 'player'), AssetManager.player_sounds)
        sound_dir: str = os.path.join(AssetManager.sounds_dir, 'fx', 'player')
        AssetManager.player_sounds['attack 2'] = AssetManager.pitch_shift_sound(os.path.join(sound_dir, 'attack 1.wav'), 2)
        AssetManager.player_sounds['attack 3'] = AssetManager.pitch_shift_sound(os.path.join(sound_dir, 'attack 1.wav'), 4)
        AssetManager.player_sounds['air attack'] = AssetManager.pitch_shift_sound(os.path.join(sound_dir, 'attack 1.wav'), 8)
    
    @staticmethod
    def load_all_music_paths() -> None:
        """Load all music paths into core_sounds dict."""
        for file in os.listdir(AssetManager.music_dir):
            if file.endswith('.ogg'):
                track_name = file.replace('.ogg','')
                AssetManager.core_music[track_name] = os.path.join(AssetManager.music_dir, file)
        
    @staticmethod
    def unload_level_assets() -> None:
        """Unload any level specific assets."""
        AssetManager.level_fonts.clear()
        AssetManager.level_sounds.clear()
        AssetManager.level_sprites.clear()
        AssetManager.level_enemies_animations.clear()
        AssetManager.level_enemies_sounds.clear()
        
    @staticmethod
    def unload_core_assets() -> None:
        """Unload core assets."""
        AssetManager.core_fonts.clear()
        AssetManager.core_sounds.clear()
        AssetManager.core_sprites.clear()
        AssetManager.core_music.clear()
        AssetManager.player_animations.clear()
        
    @staticmethod
    def unload_player_assets() -> None:
        """Unload player assets."""
        AssetManager.player_animations.clear()
        AssetManager.player_sounds.clear()
        
    # PER LEVEL LOADING/UNLOADING
    @staticmethod
    def load_level_assets(level_name: str) -> None:
        """Load level specific assets.
        Args:
            level_name (str): The name of the level to load the assets for.
        """
        # Make sure to unload any existing level assets first
        AssetManager.unload_level_assets()
        # Call level specific loading functions
        match(level_name):
            case 'test_level':
                AssetManager.load_test_level_assets()
            case 'level_1':
                AssetManager.load_level_1_assets()
            case 'level_2':
                AssetManager.load_level_2_assets()
            case _:
                print(f"No asset loading function defined for level: {level_name}")
                
    @staticmethod
    def load_test_level_assets() -> None:
        """Load test level assets."""
        pass
    
    @staticmethod
    def load_level_1_assets() -> None:
        """Load level 1 assets."""
        pass
    
    @staticmethod
    def load_level_2_assets() -> None:
        """Load level 2 assets."""
        pass
                
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
        
    @staticmethod
    def pitch_shift_sound(sound_path: str, semitones: float) -> pygame.mixer.Sound:
        sound = AudioSegment.from_file(sound_path)
        
        # Change pitch
        new_sample_rate = int(sound.frame_rate * (2.0 ** (semitones / 12.0)))
        new_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        new_sound = new_sound.set_frame_rate(44100)
        
        # Export to bytes and load into pygame Sound
        sound_bytes = io.BytesIO()
        new_sound.export(sound_bytes, format='wav')
        sound_bytes.seek(0)
        
        return pygame.mixer.Sound(sound_bytes)
    
    # HELPERS
    @staticmethod
    def load_animations_folder(folder_path: str, save_dict: dict[str, list[pygame.Surface]]) -> None:
        """Load all animations in a folder into the provided dictionary.
        Args:
            folder_path (str): Path to the folder containing animation subfolders.
            save_dict (dict): Dictionary to save animations into.
        """
        for animation in os.listdir(folder_path):
            # Path and name
            anim_path = os.path.join(folder_path, animation)
            type = animation.split('.')[-1] 
            name = animation.lower().replace(f".{type}", '')
            
            # Getting num frames and size from image height, assuming
            # all frames are square and sheet is one row.
            anim_image = pygame.image.load(anim_path).convert_alpha()
            image_w, image_h = anim_image.get_size()
            frame_count = image_w // image_h
            frame_size = (image_h, image_h)
            
            # Create spritesheet and parse frames
            anim_sheet = Spritesheet(anim_path, frame_count=frame_count, frame_size=frame_size)
            save_dict[name] = anim_sheet.parse_frames()
            
    @staticmethod       
    def load_sounds_folder(folder_path: str, save_dict: dict[str, pygame.mixer.Sound]) -> None:
        """Load all sounds in a folder into the provided dictionary.
        Args:
            folder_path (str): Path to the folder containing sound files.
            save_dict (dict): Dictionary to save sounds into.
        """
        for sound in os.listdir(folder_path):
            sound_path = os.path.join(folder_path, sound)
            type = sound.split('.')[-1]
            name = sound.lower().replace(f".{type}", '')
            save_dict[name] = pygame.mixer.Sound(sound_path)