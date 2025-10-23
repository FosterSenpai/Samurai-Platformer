# title_state.py
# Title screen state for the game.
# Author: Foster Rae
# Created: 23-10-2025
# Last Modified: 23-10-2025
import pygame
from scripts.screen_states.screen_state import State
from scripts.utilities.text import Text
from scripts.utilities.asset_manager import AssetManager

class TitleState(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.bg0 = AssetManager.core_sprites['bg0']
        self.bg1 = AssetManager.core_sprites['bg1']
        self.bg2 = AssetManager.core_sprites['bg2']
        self.bg0_x, self.bg1_x, self.bg2_x = 0, 0, 0 # Bg x positions for scrolling
        
        # Load and play music
        pygame.mixer.music.load(AssetManager.core_sounds['evening mood'])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1) # Loop

    def update(self, delta_time: float, actions: dict) -> None:
        self.scroll_bg(delta_time)
        self.game.controller.reset_actions()
    
    def render(self, surface) -> None:
        # Draw background
        # Drawing each image a second time offset to remove scoll seams
        surface.blit(self.bg0, (self.bg0_x, 0))
        surface.blit(self.bg0, (self.bg0_x + self.bg0.get_width(), 0))
        surface.blit(self.bg1, (self.bg1_x, 0))
        surface.blit(self.bg1, (self.bg1_x + self.bg1.get_width(), 0))
        surface.blit(self.bg2, (self.bg2_x, 0))
        surface.blit(self.bg2, (self.bg2_x + self.bg2.get_width(), 0))
        # Temporary text
        Text.draw_text(surface, "LOFI SAMURAI", (0, 0, 0), 
                      surface.get_width() // 2, 30)

    def scroll_bg(self, delta_time):
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