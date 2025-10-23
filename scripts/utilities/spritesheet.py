# spritesheet.py
# Class to handle loading images from sprite sheets.
# Author: Foster Rae
# Created: 23-10-2025
# Last Modified: 23-10-2025
import pygame
import json

class Spritesheet:
    def __init__(self, filename: str, colorkey: tuple[int,int,int] | None = None) -> None:
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        self.colorkey = colorkey
        # Parse json metadata
        self.meta_data = self.filename.replace('.png', '.json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        
    def get_sprite(self, x: int, y: int, w: int, h: int):
        sprite = pygame.Surface((w,h), pygame.SRCALPHA) # Prepare empty surface
        if self.colorkey is not None:
            sprite.set_colorkey(self.colorkey)
        # Cut out sprite with blit
        sprite.blit(self.sprite_sheet,(0,0),(x,y,w,h))
        return sprite
    
    def parse_spritesheet(self):
        """Parses entire spritesheet extracting images from the provided metadata.
        Returns:
            dict: Dictionary containing name - image pairs.
        """
        sprites = {}
        # Fill up sprites dict with name-image pairs
        # Software im generating json files with returns list of dicts
        for sprite_data in self.data:
            sprites[sprite_data['name']] = self.get_sprite(sprite_data['x'], sprite_data['y'],
                                                           sprite_data['width'], sprite_data['height'])
        return sprites