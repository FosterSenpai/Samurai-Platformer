# text.py
# Utility functions for rendering text.
# Author: Foster Rae
# Created: 18-10-2025
# Modified: 18-10-2025
import pygame
from config import Config

class Text:
    
    @staticmethod
    def draw_text(surface:pygame.Surface, text: str, colour, x, y):
        """Draw text at a location on screen.  
        Using default font right now.
        Args:
            surface (pygame.Surface): The surface to draw the text on.
            text (str): The text to draw.
            colour (_type_): The colour to render the text with.
            x (int): The x coordinate of the center of the text.
            y (_type_): The y coordinate of the center of the text.
        """
        text_surface = Config.FONT_DEFAULT.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        surface.blit(text_surface, text_rect)