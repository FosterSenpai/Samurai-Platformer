# spritesheet.py
# Class to handle loading images from sprite sheets, can load big sheets using metadata in json format or animations by passing frame count + dimensions.
# Author: Foster Rae
# Created: 23-10-2025
# Last Modified: 23-10-2025
import pygame
import json
from typing import Optional

class Spritesheet:
    def __init__(self, filename: str, frame_count: Optional[int] = None, frame_size: Optional[tuple[int,int]] = None
                 , colorkey: Optional[tuple[int,int,int]] = None) -> None:
        '''Initialize a Spritesheet object, can load entire sheets or animations.
        Args:
            filename (str): Path to the spritesheet image file.
            frame_count (Optional[int]): Number of frames in the spritesheet for animations.
            frame_size (Optional[tuple[int,int]]): Size (width, height) of each frame.
            colorkey (Optional[tuple[int,int,int]]): RGB color to be treated as transparent.
        '''
        self.filename: str = filename
        self.sprite_sheet: pygame.Surface = pygame.image.load(filename).convert_alpha()
        self.colorkey: Optional[tuple[int,int,int]] = colorkey
        self.frame_count: Optional[int] = frame_count
        self.frame_size: Optional[tuple[int,int]] = frame_size
        
    def get_sprite(self, x: int, y: int, w: int, h: int):
        sprite = pygame.Surface((w,h), pygame.SRCALPHA) # Prepare empty surface
        if self.colorkey is not None:
            sprite.set_colorkey(self.colorkey)
        # Cut out sprite with blit
        sprite.blit(self.sprite_sheet,(0,0),(x,y,w,h))
        return sprite
        
    def parse_frames(self) -> dict:
        """Parses spritesheet into individual frames for animations.
        Returns:
            dict: Dictionary containing frame index - image pairs.
        """
        frames = {}
        if self.frame_count is None or self.frame_size is None:
            raise ValueError("frame_count and frame_size must be provided to load frames.")
        # Extract frames from the spritesheet
        for i in range(self.frame_count):
            x = i * self.frame_size[0]
            y = 0 # Assuming single row spritesheet
            frame = self.get_sprite(x, y, self.frame_size[0], self.frame_size[1])
            frames[f"frame_{i}"] = frame
        return frames
    
    def parse_spritesheet(self):
        """Parses entire spritesheet extracting images from the provided metadata.
        Returns:
            dict: Dictionary containing name - image pairs.
        """
        meta_data = self.filename.replace('.png', '.json') # Should be in same dir and have same name
        with open(meta_data) as f:
            data = json.load(f)
        sprites = {}
        # Fill up sprites dict with name-image pairs
        # Software im generating json files with returns list of dicts
        for sprite_data in data:
            sprites[sprite_data['name']] = self.get_sprite(sprite_data['x'], sprite_data['y'],
                                                           sprite_data['width'], sprite_data['height'])
        return sprites