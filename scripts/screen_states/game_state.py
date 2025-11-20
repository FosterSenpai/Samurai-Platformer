# game_state.py
# Game screen state for the game, where the main gameplay occurs.
# Author: Foster Rae
# Created: 20-11-2025
import pygame
from scripts.screen_states.screen_state import State
from scripts.utilities.asset_manager import AssetManager
from scripts.entities.player import Player
from scripts.utilities.text import Text
class GameState(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        canvas_w, canvas_h = self.game.GAME_W, self.game.GAME_H
        
        # Create player
        self.player = Player(x=canvas_w // 2, y=canvas_h // 2)
        
        # Background
        self.bg0: pygame.Surface = AssetManager.core_sprites['bg0']
        self.bg1: pygame.Surface = AssetManager.core_sprites['bg1']
        self.bg2: pygame.Surface = AssetManager.core_sprites['bg2']
        self.bg0_x: float = 0.0 # Bg x positions for scrolling
        self.bg1_x: float = 0.0
        self.bg2_x: float = 0.0
        
    def on_enter(self):
        AssetManager.play_music('Morning Walk', volume=0.5)
        
    def on_resume(self):
        AssetManager.play_music('Morning Walk', volume=0.5)
        
    def update(self, delta_time: float, actions: dict) -> None:
        # Update game logic
        self.scroll_bg(delta_time)
        self.player.update(delta_time, actions)
        
        # just leaving back to title for now
        if actions.get('escape'):
            self.exit_state()
    
    def render(self, surface: pygame.Surface) -> None:
        self.draw_bg(surface)
        self.player.draw(surface)
        # TEMP DRAW FLOOR
        self.draw_floor(surface)
        
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
        
    # TEMP DRAWING FLOOR
    def draw_floor(self, surface: pygame.Surface):
        floor_y = 233
        floor_box = AssetManager.core_sprites['ui_sprite159']
        # stretch to full width
        floor_box = pygame.transform.scale(floor_box, (surface.get_width(), floor_box.get_height()))
        surface.blit(floor_box, (0, floor_y))
        
        # Draw big 'testing' text
        Text.draw_title(surface, "TESTING GROUNDS", surface.get_width() // 2, surface.get_height() // 8 * 6)
        
        