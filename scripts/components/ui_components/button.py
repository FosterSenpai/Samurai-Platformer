# button.py
# UI Button component with hover and click states, takes either image or color in constructor.
# Author: Foster Rae
# Created: 20-11-2025
import pygame
from typing import Optional, Callable
from scripts.utilities.asset_manager import AssetManager

class Button:
    def __init__(self, pos: tuple[int, int], display_text: Optional[str], callback: Optional[Callable] = None, image: Optional[pygame.Surface] = None, color: Optional[tuple[int, int, int]] = None, size: Optional[tuple[int, int]] = None) -> None:
        """Initializes a UI Button, either image-based or color-based. (Color buttons require size)
        Args:
            pos (tuple[int, int]): The (x, y) position of the button.
            display_text (str): The text to display on the button.
            callback (Optional[Callable], optional): Function to call when clicked. Defaults to None.
            image (Optional[pygame.Surface], optional): The image for the button. Defaults to None.
            color (Optional[tuple[int, int, int]], optional): The color for the button. Defaults to None.
            size (Optional[tuple[int, int]], optional): The size (width, height) for color buttons. Defaults to None.
        """
        if color is None and image is None:
            raise ValueError("Either color or image must be provided.")
        
        # Position and size
        self.x: int = pos[0]
        self.y: int = pos[1]
        if size is not None:
            self.w: int = size[0]
            self.h: int = size[1]
        else:
            self.w: int = image.get_width() if image else 0
            self.h: int = image.get_height() if image else 0
        
        # Content
        self.color: Optional[tuple[int, int, int]] = color
        self.image: Optional[pygame.Surface] = image
        self.is_clicked: bool = False
        self.is_hovered: bool = False
        self.callback: Optional[Callable] = callback
        self.click_sound: pygame.mixer.Sound = AssetManager.core_sounds['button_click']
        
        # Text setup
        if display_text is not None:
            self.display_text: str = display_text
            self.font: pygame.font.Font = AssetManager.core_fonts['default']
            self.text_surface_normal: pygame.Surface = self.font.render(self.display_text, True, (27, 34, 54))
            self.text_surface_hover: pygame.Surface = self.font.render(self.display_text, True, (77, 84, 84))
            self.text_surface_clicked: pygame.Surface = self.font.render(self.display_text, True, (177, 184, 204))
            self.text_rect: pygame.Rect = self.text_surface_normal.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2 - 4))
        
    def draw(self, surface: pygame.Surface) -> None:
        # Drawing the button and darkening based on state
        if self.image:
            display_image = self.image
            if self.is_clicked:
                display_image = self.darken_image(self.image, amount=60)
            elif self.is_hovered:
                display_image = self.darken_image(self.image, amount=30)
            surface.blit(display_image, (self.x, self.y))
        elif self.color:
            display_color = self.color
            if self.is_clicked:
                display_color = self.darken_color(self.color, amount=60)
            elif self.is_hovered:
                display_color = self.darken_color(self.color, amount=30)
            pygame.draw.rect(surface, display_color, (self.x, self.y, self.w, self.h))
            
        # Draw text
        if self.display_text:
            if self.is_clicked:
                surface.blit(self.text_surface_clicked, self.text_rect)
            elif self.is_hovered:
                surface.blit(self.text_surface_hover, self.text_rect)
            else:
                surface.blit(self.text_surface_normal, self.text_rect)
    
    def update(self, mouse_pos: tuple[int, int], mouse_pressed: bool) -> None:
        self.is_hovered = self.check_hovered(mouse_pos)
                
        # Handle click
        was_clicked = self.is_clicked # Store previous state (for stopping click spam)
        if self.is_hovered and mouse_pressed and not was_clicked:
            self.click_sound.play()
            self.is_clicked = True
            if self.callback:
                self.callback()
        elif not mouse_pressed:
            self.is_clicked = False # Reset state
    
    def darken_color(self, color: tuple[int, int, int], amount: int = 30) -> tuple[int, int, int]:
        r = max(0, color[0] - amount)
        g = max(0, color[1] - amount)
        b = max(0, color[2] - amount)
        return (r, g, b)
    
    def darken_image(self, image: pygame.Surface, amount: int = 30) -> pygame.Surface:
        darkened_image = image.copy()
        dark_overlay = pygame.Surface(image.get_size()).convert_alpha()
        dark_overlay.fill((0, 0, 0, amount))
        darkened_image.blit(dark_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        return darkened_image
    
    def check_hovered(self, mouse_pos: tuple[int, int]) -> bool:
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        return rect.collidepoint(mouse_pos)
        
        
    
