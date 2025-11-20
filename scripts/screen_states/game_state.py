# game_state.py
# Game screen state for the game, where the main gameplay occurs.
# Author: Foster Rae
# Created: 20-11-2025
import pygame
from scripts.screen_states.screen_state import State
from scripts.utilities.asset_manager import AssetManager
class GameState(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        canvas_w, canvas_h = self.game.GAME_W, self.game.GAME_H
        
        # Background
        self.bg0: pygame.Surface = AssetManager.core_sprites['bg0']
        self.bg1: pygame.Surface = AssetManager.core_sprites['bg1']
        self.bg2: pygame.Surface = AssetManager.core_sprites['bg2']
        self.bg0_x: float = 0.0 # Bg x positions for scrolling
        self.bg1_x: float = 0.0
        self.bg2_x: float = 0.0
        
        # Load and play music
        pygame.mixer.music.load(AssetManager.core_sounds['evening mood'])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1) # Loop
        
    def update(self, delta_time: float, actions: dict) -> None:
        # Update game logic
        self.scroll_bg(delta_time)
        
        # just leaving back to title for now
        if actions.get('escape'):
            self.game.screen_state_stack.pop()  # Return to previous state (title)
    
    def render(self, surface: pygame.Surface) -> None:
        self.draw_bg(surface)
        
    def scroll_bg(self, delta_time: float):
        # Scroll speeds
        bg0_speed, bg1_speed, bg2_speed = 10,20,30
        # Scroll bg to left
        self.bg0_x -= bg0_speed * delta_time
        self.bg1_x -= bg1_speed * delta_time
        self.bg2_x -= bg2_speed * delta_time
        # Wrap
        bg_width = self.bg0.get_width()
        if self.bg0_x <= -bg_width:
            self.bg0_x = 0
        if self.bg1_x <= -bg_width:
            self.bg1_x = 0
        if self.bg2_x <= -bg_width:
            self.bg2_x = 0
            
    def draw_bg(self, surface: pygame.Surface):
        # Drawing each image a second time offset to remove scoll seams
        surface.blit(self.bg0, (self.bg0_x, 0))
        surface.blit(self.bg0, (self.bg0_x + self.bg0.get_width(), 0))
        surface.blit(self.bg1, (self.bg1_x, 0))
        surface.blit(self.bg1, (self.bg1_x + self.bg1.get_width(), 0))
        surface.blit(self.bg2, (self.bg2_x, 0))
        surface.blit(self.bg2, (self.bg2_x + self.bg2.get_width(), 0))