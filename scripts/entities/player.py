# player.py
# The class for the player entity, handles player stats and rendering.
# Author: Foster Rae
# Created: 18-10-2025
# Last Modified: 18-10-2025
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))