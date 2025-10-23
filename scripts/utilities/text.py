# text.py
# Utility functions for rendering text.
# Author: Foster Rae
# Created: 18-10-2025
# Modified: 18-10-2025
import pygame
from scripts.utilities.asset_manager import AssetManager

class Text:
    
    @staticmethod
    def draw_text(surface:pygame.Surface, text: str, colour, x, y):
        """Draw text at a location on screen.  
        Args:
            surface (pygame.Surface): The surface to draw the text on.
            text (str): The text to draw.
            colour (_type_): The colour to render the text with.
            x (int): The x coordinate of the center of the text.
            y (_type_): The y coordinate of the center of the text.
        """
        text_surface = AssetManager.core_fonts['default'].render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        surface.blit(text_surface, text_rect)
        
    @staticmethod
    def draw_title(surface: pygame.Surface, text: str, x: int, y: int):
        """Draw text at a location on screen with large title font.
        Args:
            surface (pygame.Surface): The surface to draw the text on.
            text (str): The text to draw.
            x (int): The x coordinate of the center of the text.
            y (int): The y coordinate of the center of the text.
        """
        text_surface = AssetManager.core_fonts['title'].render(text, True, (175,175,175))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        surface.blit(text_surface, text_rect)
    
    @staticmethod
    def draw_small(surface: pygame.Surface, text: str, x: int, y: int):
        """Draw text at a location on screen with small font.
        Args:
            surface (pygame.Surface): The surface to draw the text on.
            text (str): The text to draw.
            x (int): The x coordinate of the center of the text.
            y (int): The y coordinate of the center of the text.
        """
        text_surface = AssetManager.core_fonts['subtitle'].render(text, True, (200,200,200))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        surface.blit(text_surface, text_rect)